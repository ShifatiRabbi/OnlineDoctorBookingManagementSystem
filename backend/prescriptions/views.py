from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from .services import create_prescription_service, get_prescription_service, get_patient_prescriptions_service
from .models import Medicine, Test
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_prescription(request):
    """
    API endpoint to create a new prescription
    """
    try:
        data = json.loads(request.body)
        success, result = create_prescription_service(data, request)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': 'Prescription created successfully',
                'data': {
                    'id': result.id,
                    'appointment_id': result.appointment.id,
                    'patient': result.patient.name,
                    'doctor': f"Dr. {result.doctor.user.get_full_name()}",
                    'printable_key': result.printable_key
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_prescription(request, prescription_id):
    """
    API endpoint to get prescription details
    """
    try:
        success, result = get_prescription_service(prescription_id, request)
        
        if success:
            return JsonResponse({
                'success': True,
                'data': {
                    'id': result.id,
                    'appointment_id': result.appointment.id,
                    'patient': {
                        'id': result.patient.id,
                        'name': result.patient.name,
                        'phone': result.patient.phone
                    },
                    'doctor': {
                        'id': result.doctor.id,
                        'name': f"Dr. {result.doctor.user.get_full_name()}",
                        'degrees': result.doctor.degrees
                    },
                    'items': result.items,
                    'tests': result.tests,
                    'advice': result.advice,
                    'created_at': result.created_at,
                    'printable_key': result.printable_key
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
def get_patient_prescriptions(request, patient_id):
    """
    API endpoint to get all prescriptions for a patient
    """
    try:
        success, result = get_patient_prescriptions_service(patient_id, request)
        
        if success:
            prescriptions = []
            for prescription in result:
                prescriptions.append({
                    'id': prescription.id,
                    'date': prescription.created_at.strftime('%Y-%m-%d'),
                    'doctor': f"Dr. {prescription.doctor.user.get_full_name()}",
                    'items_count': len(prescription.items),
                    'tests_count': len(prescription.tests)
                })
            
            return JsonResponse({
                'success': True,
                'data': prescriptions
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
def list_medicines(request):
    """
    API endpoint to list all medicines
    """
    try:
        medicines = Medicine.objects.all()
        medicine_list = []
        
        for medicine in medicines:
            medicine_list.append({
                'id': medicine.id,
                'name': medicine.name,
                'generic': medicine.generic,
                'strength': medicine.strength,
                'form': medicine.form
            })
        
        return JsonResponse({
            'success': True,
            'data': medicine_list
        })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_tests(request):
    """
    API endpoint to list all tests
    """
    try:
        tests = Test.objects.all()
        test_list = []
        
        for test in tests:
            test_list.append({
                'id': test.id,
                'name': test.name,
                'category': test.category
            })
        
        return JsonResponse({
            'success': True,
            'data': test_list
        })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)