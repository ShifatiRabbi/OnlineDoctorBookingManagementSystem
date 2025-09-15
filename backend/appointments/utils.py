from datetime import datetime, timedelta

def generate_time_slots(start_time, end_time, duration):
    """
    Generate time slots between start_time and end_time with given duration
    """
    time_slots = []
    start = datetime.strptime(start_time, '%H:%M')
    end = datetime.strptime(end_time, '%H:%M')
    
    while start < end:
        time_slots.append(start.strftime('%H:%M'))
        start += timedelta(minutes=duration)
    
    return time_slots

def is_time_slot_available(doctor, branch, date, time):
    """
    Check if a time slot is available for booking
    """
    from .models import Appointment
    
    # Check if appointment already exists
    existing_appointment = Appointment.objects.filter(
        doctor=doctor,
        branch=branch,
        date=date,
        time=time,
        status__in=['PENDING', 'CONFIRMED', 'CHECKED_IN']
    ).exists()
    
    return not existing_appointment