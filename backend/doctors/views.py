from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.http import JsonResponse
from .services import create_doctor_service, update_doctor_service, create_doctor_schedule_service, generate_time_slots_service
from .models import Doctor, Specialty, DoctorSchedule
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_doctor(request):
    """
    API endpoint to create a new doctor
    """
    try:
        data = json.loads(request.body)
        success, result = create_doctor_service(data, request)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': 'Doctor created successfully',
                'data': {
                    'id': result.id,
                    'user_id': result.user.id,
                    'degrees': result.degrees,
                    'fee': float(result.fee),
                    'default_branch': result.default_branch.id
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
@permission_classes([IsAuthenticated, IsAdminUser])
def update_doctor(request, doctor_id):
    """
    API endpoint to update a doctor
    """
    try:
        data = json.loads(request.body)
        success, result = update_doctor_service(doctor_id, data, request)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': 'Doctor updated successfully',
                'data': {
                    'id': result.id,
                    'user_id': result.user.id,
                    'degrees': result.degrees,
                    'fee': float(result.fee),
                    'default_branch': result.default_branch.id,
                    'active': result.active
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

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_doctor_schedule(request, doctor_id):
    """
    API endpoint to create a doctor schedule
    """
    try:
        data = json.loads(request.body)
        success, result = create_doctor_schedule_service(doctor_id, data, request)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': 'Doctor schedule created successfully',
                'data': {
                    'id': result.id,
                    'doctor': result.doctor.id,
                    'branch': result.branch.id,
                    'weekday': result.weekday,
                    'start_time': result.start_time.strftime('%H:%M:%S'),
                    'end_time': result.end_time.strftime('%H:%M:%S'),
                    'slot_duration': result.slot_duration,
                    'capacity': result.capacity
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_time_slots_view(request, doctor_id, branch_id):
    """
    API endpoint to generate time slots for a doctor
    """
    try:
        date = request.GET.get('date')
        if not date:
            return JsonResponse({
                'success': False,
                'error': 'Date parameter is required'
            }, status=400)
        
        success, result = generate_time_slots_service(doctor_id, branch_id, date, request)
        
        if success:
            slots_data = []
            for slot in result:
                slots_data.append({
                    'id': slot.id,
                    'doctor': slot.doctor.id,
                    'branch': slot.branch.id,
                    'date': slot.date.strftime('%Y-%m-%d'),
                    'start_time': slot.start_time.strftime('%H:%M:%S'),
                    'end_time': slot.end_time.strftime('%H:%M:%S'),
                    'capacity': slot.capacity,
                    'booked_count': slot.booked_count,
                    'available': slot.capacity - slot.booked_count
                })
            
            return JsonResponse({
                'success': True,
                'message': f'{len(slots_data)} time slots generated successfully',
                'data': slots_data
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
def list_doctors(request):
    """
    API endpoint to list all doctors
    """
    try:
        doctors = Doctor.objects.filter(active=True)
        doctor_list = []
        
        for doctor in doctors:
            specialties = [s.name for s in doctor.specialties.all()]
            doctor_list.append({
                'id': doctor.id,
                'name': f"Dr. {doctor.user.get_full_name()}",
                'degrees': doctor.degrees,
                'specialties': specialties,
                'fee': float(doctor.fee),
                'default_branch': doctor.default_branch.id,
                'default_branch_name': doctor.default_branch.name
            })
        
        return JsonResponse({
            'success': True,
            'data': doctor_list
        })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)