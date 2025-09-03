from .models import Prescription, PrescriptionTemplate, Medicine, Test
from appointments.models import Appointment
from doctors.models import Doctor
from patients.models import Patient
from branches.models import Branch
from audit.models import AuditLog
import json
import uuid

def create_prescription_service(data, request):
    """
    Service function to create a new prescription
    """
    try:
        # Validate required fields
        required_fields = ['appointment_id', 'items', 'tests']
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        # Get appointment
        try:
            appointment = Appointment.objects.get(id=data['appointment_id'])
        except Appointment.DoesNotExist:
            return False, "Appointment not found"
        
        # Check if prescription already exists for this appointment
        if Prescription.objects.filter(appointment=appointment).exists():
            return False, "Prescription already exists for this appointment"
        
        # Create prescription
        prescription = Prescription(
            appointment=appointment,
            doctor=appointment.doctor,
            patient=appointment.patient,
            items=data['items'],
            tests=data['tests'],
            advice=data.get('advice', ''),
            printable_key=str(uuid.uuid4()).replace('-', '')  # Generate unique key for PDF access
        )
        prescription.save()
        
        # Update appointment status to completed
        appointment.status = 'COMPLETED'
        appointment.save()
        
        # Create audit log
        AuditLog.objects.create(
            actor=request.user if request.user.is_authenticated else None,
            action="CREATE_PRESCRIPTION",
            target_type="Prescription",
            target_id=prescription.id,
            diff=data,
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return True, prescription
        
    except Exception as e:
        return False, str(e)

def get_prescription_service(prescription_id, request):
    """
    Service function to get prescription details
    """
    try:
        # Get prescription
        try:
            prescription = Prescription.objects.get(id=prescription_id)
        except Prescription.DoesNotExist:
            return False, "Prescription not found"
        
        return True, prescription
        
    except Exception as e:
        return False, str(e)

def get_patient_prescriptions_service(patient_id, request):
    """
    Service function to get all prescriptions for a patient
    """
    try:
        # Get patient
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return False, "Patient not found"
        
        # Get prescriptions
        prescriptions = Prescription.objects.filter(patient=patient).order_by('-created_at')
        
        return True, prescriptions
        
    except Exception as e:
        return False, str(e)