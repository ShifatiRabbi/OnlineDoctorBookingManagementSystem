from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from .services import create_appointment_service, send_appointment_sms_service
from .models import Appointment
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_appointment(request):
    """
    API endpoint to create a new appointment
    """
    try:
        data = json.loads(request.body)
        success, result = create_appointment_service(data, request)
        
        if success:
            # Send confirmation SMS
            sms_success, sms_result = send_appointment_sms_service(result)
            
            if sms_success:
                return JsonResponse({
                    'success': True,
                    'message': 'Appointment created successfully and SMS sent',
                    'data': {
                        'id': result.id,
                        'patient': result.patient.name,
                        'doctor': f"Dr. {result.doctor.user.get_full_name()}",
                        'date': result.date,
                        'time': result.time,
                        'status': result.status
                    }
                }, status=201)
            else:
                return JsonResponse({
                    'success': True,
                    'message': 'Appointment created but SMS failed',
                    'data': {
                        'id': result.id,
                        'patient': result.patient.name,
                        'doctor': f"Dr. {result.doctor.user.get_full_name()}",
                        'date': result.date,
                        'time': result.time,
                        'status': result.status
                    },
                    'sms_error': sms_result
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
def get_appointment(request, appointment_id):
    """
    API endpoint to get appointment details
    """
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        
        return JsonResponse({
            'success': True,
            'data': {
                'id': appointment.id,
                'patient': {
                    'id': appointment.patient.id,
                    'name': appointment.patient.name,
                    'phone': appointment.patient.phone
                },
                'doctor': {
                    'id': appointment.doctor.id,
                    'name': f"Dr. {appointment.doctor.user.get_full_name()}"
                },
                'branch': {
                    'id': appointment.branch.id,
                    'name': appointment.branch.name
                },
                'date': appointment.date,
                'time': appointment.time,
                'status': appointment.status,
                'notes': appointment.notes,
                'created_at': appointment.created_at
            }
        })
        
    except Appointment.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Appointment not found'
        }, status=404)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)