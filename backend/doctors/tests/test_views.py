import pytest
import json
from django.urls import reverse
from tests.factories import DoctorFactory, SpecialtyFactory, BranchFactory

@pytest.mark.django_db
class TestDoctorsViews:
    def test_create_doctor(self, authenticated_admin_client):
        from tests.factories import DoctorUserFactory
        
        user = DoctorUserFactory()
        branch = BranchFactory()
        specialty = SpecialtyFactory()
        
        url = reverse('create_doctor')
        data = {
            'user_id': user.id,
            'degrees': 'MBBS, FCPS',
            'fee': 800.00,
            'default_branch_id': branch.id,
            'specialties': [specialty.id]
        }
        
        response = authenticated_admin_client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        assert response.json()['success'] is True
    
    def test_list_doctors(self, authenticated_admin_client):
        DoctorFactory.create_batch(2)
        url = reverse('list_doctors')
        
        response = authenticated_admin_client.get(url)
        
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert len(response.json()['data']) >= 2
    
    def test_create_doctor_schedule(self, authenticated_admin_client):
        doctor = DoctorFactory()
        branch = BranchFactory()
        
        url = reverse('create_doctor_schedule', args=[doctor.id])
        data = {
            'branch_id': branch.id,
            'weekday': 0,  # Monday
            'start_time': '09:00:00',
            'end_time': '17:00:00',
            'slot_duration': 30,
            'capacity': 10
        }
        
        response = authenticated_admin_client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        assert response.json()['success'] is True