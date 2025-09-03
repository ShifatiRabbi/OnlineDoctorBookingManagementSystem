from .models import ReportCache
from appointments.models import Appointment
from doctors.models import Doctor
from branches.models import Branch
from datetime import datetime, timedelta
import json

def generate_daily_report_service(date, branch_id=None):
    """
    Service function to generate daily report
    """
    try:
        # Parse date
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        
        # Get appointments for the date
        appointments = Appointment.objects.filter(date=date_obj)
        
        if branch_id:
            try:
                branch = Branch.objects.get(id=branch_id)
                appointments = appointments.filter(branch=branch)
            except Branch.DoesNotExist:
                return False, "Branch not found"
        
        # Calculate statistics
        total_appointments = appointments.count()
        confirmed_appointments = appointments.filter(status='CONFIRMED').count()
        completed_appointments = appointments.filter(status='COMPLETED').count()
        cancelled_appointments = appointments.filter(status='CANCELLED').count()
        
        # Group by doctor
        doctor_stats = []
        doctors = Doctor.objects.filter(active=True)
        
        for doctor in doctors:
            doctor_appointments = appointments.filter(doctor=doctor)
            if doctor_appointments.exists():
                doctor_stats.append({
                    'doctor_id': doctor.id,
                    'doctor_name': f"Dr. {doctor.user.get_full_name()}",
                    'total': doctor_appointments.count(),
                    'confirmed': doctor_appointments.filter(status='CONFIRMED').count(),
                    'completed': doctor_appointments.filter(status='COMPLETED').count(),
                    'cancelled': doctor_appointments.filter(status='CANCELLED').count()
                })
        
        # Prepare report data
        report_data = {
            'date': date,
            'branch_id': branch_id,
            'total_appointments': total_appointments,
            'confirmed_appointments': confirmed_appointments,
            'completed_appointments': completed_appointments,
            'cancelled_appointments': cancelled_appointments,
            'doctor_stats': doctor_stats
        }
        
        # Cache the report
        aggregation_key = f"daily_report_{date}"
        if branch_id:
            aggregation_key += f"_{branch_id}"
        
        report_cache, created = ReportCache.objects.update_or_create(
            aggregation_key=aggregation_key,
            defaults={
                'json_data': report_data,
                'period': 'daily'
            }
        )
        
        return True, report_data
        
    except Exception as e:
        return False, str(e)

def generate_monthly_report_service(year, month, branch_id=None):
    """
    Service function to generate monthly report
    """
    try:
        # Get first and last day of the month
        first_day = datetime(year, month, 1).date()
        if month == 12:
            last_day = datetime(year + 1, 1, 1).date() - timedelta(days=1)
        else:
            last_day = datetime(year, month + 1, 1).date() - timedelta(days=1)
        
        # Get appointments for the month
        appointments = Appointment.objects.filter(date__range=[first_day, last_day])
        
        if branch_id:
            try:
                branch = Branch.objects.get(id=branch_id)
                appointments = appointments.filter(branch=branch)
            except Branch.DoesNotExist:
                return False, "Branch not found"
        
        # Calculate statistics
        total_appointments = appointments.count()
        confirmed_appointments = appointments.filter(status='CONFIRMED').count()
        completed_appointments = appointments.filter(status='COMPLETED').count()
        cancelled_appointments = appointments.filter(status='CANCELLED').count()
        
        # Group by date
        date_stats = []
        current_date = first_day
        while current_date <= last_day:
            date_appointments = appointments.filter(date=current_date)
            if date_appointments.exists():
                date_stats.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'total': date_appointments.count(),
                    'confirmed': date_appointments.filter(status='CONFIRMED').count(),
                    'completed': date_appointments.filter(status='COMPLETED').count(),
                    'cancelled': date_appointments.filter(status='CANCELLED').count()
                })
            current_date += timedelta(days=1)
        
        # Prepare report data
        report_data = {
            'year': year,
            'month': month,
            'branch_id': branch_id,
            'total_appointments': total_appointments,
            'confirmed_appointments': confirmed_appointments,
            'completed_appointments': completed_appointments,
            'cancelled_appointments': cancelled_appointments,
            'date_stats': date_stats
        }
        
        # Cache the report
        aggregation_key = f"monthly_report_{year}_{month}"
        if branch_id:
            aggregation_key += f"_{branch_id}"
        
        report_cache, created = ReportCache.objects.update_or_create(
            aggregation_key=aggregation_key,
            defaults={
                'json_data': report_data,
                'period': 'monthly'
            }
        )
        
        return True, report_data
        
    except Exception as e:
        return False, str(e)