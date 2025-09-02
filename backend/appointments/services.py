from django.http import JsonResponse # type: ignore
from .models import Appointment
from patients.models import Patient
from doctors.models import Doctor, TimeSlot
from branches.models import Branch
from accounts.models import User
from sms.models import SMSMessage
from audit.models import AuditLog
import json
from datetime import datetime

def create_appointment_service(data, request):
    """
    Service function to create a new appointment
    """
    try:
        # Validate required fields
        required_fields = ['patient_id', 'doctor_id', 'branch_id', 'date', 'time']
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        # Check if patient exists
        try:
            patient = Patient.objects.get(id=data['patient_id'])
        except Patient.DoesNotExist:
            return False, "Patient not found"
        
        # Check if doctor exists
        try:
            doctor = Doctor.objects.get(id=data['doctor_id'])
        except Doctor.DoesNotExist:
            return False, "Doctor not found"
        
        # Check if branch exists
        try:
            branch = Branch.objects.get(id=data['branch_id'])
        except Branch.DoesNotExist:
            return False, "Branch not found"
        
        # Check if timeslot is available
        date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
        time_obj = datetime.strptime(data['time'], '%H:%M:%S').time()
        
        try:
            timeslot = TimeSlot.objects.get(
                doctor=doctor,
                branch=branch,
                date=date_obj,
                start_time=time_obj
            )
            
            if timeslot.booked_count >= timeslot.capacity:
                return False, "Time slot is fully booked"
                
        except TimeSlot.DoesNotExist:
            return False, "Time slot not available"
        
        # Create appointment
        appointment = Appointment(
            patient=patient,
            doctor=doctor,
            branch=branch,
            date=date_obj,
            time=time_obj,
            status='PENDING',
            created_by=request.user if request.user.is_authenticated else None,
            notes=data.get('notes', '')
        )
        appointment.save()
        
        # Update timeslot booked count
        timeslot.booked_count += 1
        timeslot.save()
        
        # Create audit log
        AuditLog.objects.create(
            actor=request.user if request.user.is_authenticated else None,
            action="CREATE_APPOINTMENT",
            target_type="Appointment",
            target_id=appointment.id,
            diff=data,
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return True, appointment
        
    except Exception as e:
        return False, str(e)

def send_appointment_sms_service(appointment):
    """
    Service function to send SMS for appointment confirmation
    """
    try:
        # Create SMS content
        content = f"Your appointment with Dr. {appointment.doctor.user.get_full_name()} is confirmed for {appointment.date} at {appointment.time}. Branch: {appointment.branch.name}"
        
        # Create SMS record
        sms = SMSMessage(
            to=appointment.patient.phone,
            content=content,
            type='APPOINTMENT',
            status='PENDING'
        )
        sms.save()
        
        # Here you would integrate with your SMS provider
        # For now, we'll just mark it as sent
        sms.status = 'SENT'
        sms.provider_id = 'SIMULATED'
        sms.save()
        
        return True, "SMS sent successfully"
        
    except Exception as e:
        return False, str(e)