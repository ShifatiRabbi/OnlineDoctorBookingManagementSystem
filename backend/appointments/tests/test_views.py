import pytest
import json
from django.urls import reverse
from tests.factories import AppointmentFactory, PatientFactory, DoctorFactory, BranchFactory
from doctors.models import DoctorSchedule, TimeSlot
from datetime import datetime, timedelta

@pytest.mark.django_db
class TestAppointmentsViews:
    def test_create_appointment(self, authenticated_admin_client):
        patient = PatientFactory()
        doctor = DoctorFactory()
        branch = BranchFactory()
        
        # Create doctor schedule
        schedule = DoctorSchedule.objects.create(
            doctor=doctor,
            branch=branch,
            weekday=0,  # Monday
            start_time='09:00:00',
            end_time='17:00:00',
            slot_duration=30,
            capacity=5
        )
        
        # Create time slot
        tomorrow = datetime.now().date() + timedelta(days=1)
        time_slot = TimeSlot.objects.create(
            doctor=doctor,
            branch=branch,
            date=tomorrow,
            start_time='09:00:00',
            end_time='09:30:00',
            capacity=5,
            booked_count=0
        )
        
        url = reverse('create_appointment')
        data = {
            'patient_id': patient.id,
            'doctor_id': doctor.id,
            'branch_id': branch.id,
            'date': tomorrow.strftime('%Y-%m-%d'),
            'time': '09:00:00'
        }
        
        response = authenticated_admin_client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        assert response.json()['success'] is True
    
    def test_get_appointment(self, authenticated_admin_client):
        appointment = AppointmentFactory()
        url = reverse('get_appointment', args=[appointment.id])
        
        response = authenticated_admin_client.get(url)
        
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert response.json()['data']['patient']['name'] == appointment.patient.name