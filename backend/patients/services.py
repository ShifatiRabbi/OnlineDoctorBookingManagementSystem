from .models import Patient
from audit.models import AuditLog
import json

def create_patient_service(data, request):
    """
    Service function to create a new patient
    """
    try:
        # Validate required fields
        required_fields = ['name', 'phone']
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        # Create patient
        patient = Patient(
            name=data['name'],
            phone=data['phone'],
            address=data.get('address', ''),
            dob=data.get('dob'),
            gender=data.get('gender', '')
        )
        patient.save()
        
        # Create audit log
        AuditLog.objects.create(
            actor=request.user if request.user.is_authenticated else None,
            action="CREATE_PATIENT",
            target_type="Patient",
            target_id=patient.id,
            diff=data,
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return True, patient
        
    except Exception as e:
        return False, str(e)

def update_patient_service(patient_id, data, request):
    """
    Service function to update a patient
    """
    try:
        # Get patient
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return False, "Patient not found"
        
        # Update fields
        if 'name' in data:
            patient.name = data['name']
        if 'phone' in data:
            patient.phone = data['phone']
        if 'address' in data:
            patient.address = data['address']
        if 'dob' in data:
            patient.dob = data['dob']
        if 'gender' in data:
            patient.gender = data['gender']
        
        patient.save()
        
        # Create audit log
        AuditLog.objects.create(
            actor=request.user if request.user.is_authenticated else None,
            action="UPDATE_PATIENT",
            target_type="Patient",
            target_id=patient.id,
            diff=data,
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return True, patient
        
    except Exception as e:
        return False, str(e)

def search_patients_service(phone=None, name=None):
    """
    Service function to search patients by phone or name
    """
    try:
        patients = Patient.objects.all()
        
        if phone:
            patients = patients.filter(phone__icontains=phone)
        
        if name:
            patients = patients.filter(name__icontains=name)
        
        return True, patients
        
    except Exception as e:
        return False, str(e)