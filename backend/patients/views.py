from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from .services import create_patient_service, update_patient_service, search_patients_service
from .models import Patient
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_patient(request):
    """
    API endpoint to create a new patient
    """
    try:
        data = json.loads(request.body)
        success, result = create_patient_service(data, request)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': 'Patient created successfully',
                'data': {
                    'id': result.id,
                    'name': result.name,
                    'phone': result.phone
                }
            }, status=201)
        else:
            return JsonResponse({
                'success': False,
                'error': result
            }, status=400)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_patient(request, patient_id):
    """
    API endpoint to update a patient
    """
    try:
        data = json.loads(request.body)
        success, result = update_patient_service(patient_id, data, request)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': 'Patient updated successfully',
                'data': {
                    'id': result.id,
                    'name': result.name,
                    'phone': result.phone
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'error': result
            }, status=400)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_patients(request):
    """
    API endpoint to search patients by phone or name
    """
    try:
        phone = request.GET.get('phone')
        name = request.GET.get('name')
        
        if not phone and not name:
            return JsonResponse({
                'success': False,
                'error': 'Phone or name parameter is required'
            }, status=400)
        
        success, result = search_patients_service(phone, name)
        
        if success:
            patient_list = []
            for patient in result:
                patient_list.append({
                    'id': patient.id,
                    'name': patient.name,
                    'phone': patient.phone,
                    'address': patient.address,
                    'dob': patient.dob,
                    'gender': patient.gender
                })
            
            return JsonResponse({
                'success': True,
                'data': patient_list
            })
        else:
            return JsonResponse({
                'success': False,
                'error': result
            }, status=400)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patient(request, patient_id):
    """
    API endpoint to get patient details
    """
    try:
        patient = Patient.objects.get(id=patient_id)
        
        return JsonResponse({
            'success': True,
            'data': {
                'id': patient.id,
                'name': patient.name,
                'phone': patient.phone,
                'address': patient.address,
                'dob': patient.dob,
                'gender': patient.gender
            }
        })
        
    except Patient.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Patient not found'
        }, status=404)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)