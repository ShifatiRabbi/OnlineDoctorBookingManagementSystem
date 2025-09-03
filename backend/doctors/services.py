from .models import Doctor, Specialty, DoctorSchedule, TimeSlot, DoctorSignature
from accounts.models import User
from branches.models import Branch
from audit.models import AuditLog
from appointments.utils import generate_time_slots
from datetime import datetime, timedelta
import json

def create_doctor_service(data, request):
    """
    Service function to create a new doctor
    """
    try:
        # Validate required fields
        required_fields = ['user_id', 'degrees', 'fee', 'default_branch_id']
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        # Check if user exists and is a doctor
        try:
            user = User.objects.get(id=data['user_id'])
            if user.role != 'DOCTOR':
                return False, "User is not a doctor"
        except User.DoesNotExist:
            return False, "User not found"
        
        # Check if doctor already exists for this user
        if Doctor.objects.filter(user=user).exists():
            return False, "Doctor profile already exists for this user"
        
        # Check if default branch exists
        try:
            default_branch = Branch.objects.get(id=data['default_branch_id'])
        except Branch.DoesNotExist:
            return False, "Default branch not found"
        
        # Create doctor
        doctor = Doctor(
            user=user,
            degrees=data['degrees'],
            fee=data['fee'],
            default_branch=default_branch,
            active=data.get('active', True)
        )
        doctor.save()
        
        # Add specialties
        if 'specialties' in data:
            for specialty_id in data['specialties']:
                try:
                    specialty = Specialty.objects.get(id=specialty_id)
                    doctor.specialties.add(specialty)
                except Specialty.DoesNotExist:
                    pass  # Skip invalid specialties
        
        # Create audit log
        AuditLog.objects.create(
            actor=request.user if request.user.is_authenticated else None,
            action="CREATE_DOCTOR",
            target_type="Doctor",
            target_id=doctor.id,
            diff=data,
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return True, doctor
        
    except Exception as e:
        return False, str(e)

def update_doctor_service(doctor_id, data, request):
    """
    Service function to update a doctor
    """
    try:
        # Get doctor
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return False, "Doctor not found"
        
        # Update fields
        if 'degrees' in data:
            doctor.degrees = data['degrees']
        if 'fee' in data:
            doctor.fee = data['fee']
        if 'active' in data:
            doctor.active = data['active']
        
        # Update default branch
        if 'default_branch_id' in data:
            try:
                default_branch = Branch.objects.get(id=data['default_branch_id'])
                doctor.default_branch = default_branch
            except Branch.DoesNotExist:
                return False, "Default branch not found"
        
        # Update specialties
        if 'specialties' in data:
            doctor.specialties.clear()
            for specialty_id in data['specialties']:
                try:
                    specialty = Specialty.objects.get(id=specialty_id)
                    doctor.specialties.add(specialty)
                except Specialty.DoesNotExist:
                    pass  # Skip invalid specialties
        
        doctor.save()
        
        # Create audit log
        AuditLog.objects.create(
            actor=request.user if request.user.is_authenticated else None,
            action="UPDATE_DOCTOR",
            target_type="Doctor",
            target_id=doctor.id,
            diff=data,
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return True, doctor
        
    except Exception as e:
        return False, str(e)

def create_doctor_schedule_service(doctor_id, data, request):
    """
    Service function to create a doctor schedule
    """
    try:
        # Validate required fields
        required_fields = ['branch_id', 'weekday', 'start_time', 'end_time', 'slot_duration']
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        # Get doctor
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return False, "Doctor not found"
        
        # Get branch
        try:
            branch = Branch.objects.get(id=data['branch_id'])
        except Branch.DoesNotExist:
            return False, "Branch not found"
        
        # Check if schedule already exists for this doctor, branch and weekday
        if DoctorSchedule.objects.filter(doctor=doctor, branch=branch, weekday=data['weekday']).exists():
            return False, "Schedule already exists for this doctor, branch and weekday"
        
        # Create doctor schedule
        schedule = DoctorSchedule(
            doctor=doctor,
            branch=branch,
            weekday=data['weekday'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            slot_duration=data['slot_duration'],
            capacity=data.get('capacity', 1)
        )
        schedule.save()
        
        # Create audit log
        AuditLog.objects.create(
            actor=request.user if request.user.is_authenticated else None,
            action="CREATE_DOCTOR_SCHEDULE",
            target_type="DoctorSchedule",
            target_id=schedule.id,
            diff=data,
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return True, schedule
        
    except Exception as e:
        return False, str(e)

def generate_time_slots_service(doctor_id, branch_id, date, request):
    """
    Service function to generate time slots for a doctor on a specific date
    """
    try:
        # Get doctor
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return False, "Doctor not found"
        
        # Get branch
        try:
            branch = Branch.objects.get(id=branch_id)
        except Branch.DoesNotExist:
            return False, "Branch not found"
        
        # Get the weekday for the given date
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        weekday = date_obj.weekday()  # Monday is 0, Sunday is 6
        
        # Get doctor schedule for this weekday and branch
        try:
            schedule = DoctorSchedule.objects.get(doctor=doctor, branch=branch, weekday=weekday)
        except DoctorSchedule.DoesNotExist:
            return False, "No schedule found for this doctor, branch and date"
        
        # Generate time slots
        start_time = schedule.start_time.strftime('%H:%M')
        end_time = schedule.end_time.strftime('%H:%M')
        time_slots = generate_time_slots(start_time, end_time, schedule.slot_duration)
        
        # Create TimeSlot records
        created_slots = []
        for slot_time in time_slots:
            time_obj = datetime.strptime(slot_time, '%H:%M').time()
            
            # Check if time slot already exists
            if not TimeSlot.objects.filter(doctor=doctor, branch=branch, date=date_obj, start_time=time_obj).exists():
                time_slot = TimeSlot(
                    doctor=doctor,
                    branch=branch,
                    date=date_obj,
                    start_time=time_obj,
                    end_time=(datetime.combine(date_obj, time_obj) + timedelta(minutes=schedule.slot_duration)).time(),
                    capacity=schedule.capacity,
                    booked_count=0
                )
                time_slot.save()
                created_slots.append(time_slot)
        
        return True, created_slots
        
    except Exception as e:
        return False, str(e)