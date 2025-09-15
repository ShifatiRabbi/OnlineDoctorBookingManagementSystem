import pytest
import json
from django.urls import reverse
from tests.factories import PatientFactory

@pytest.mark.django_db
class TestPatientsViews:
    def test_create_patient(self, authenticated_admin_client):
        url = reverse('create_patient')
        data = {
            'name': 'Test Patient',
            'phone': '+8801712345678',
            'address': '123 Test Street',
            'gender': 'M'
        }
        
        response = authenticated_admin_client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        assert response.json()['success'] is True
        assert response.json()['data']['name'] == 'Test Patient'
    
    def test_search_patients(self, authenticated_admin_client):
        PatientFactory(name='John Doe', phone='+8801711111111')
        PatientFactory(name='Jane Smith', phone='+8801722222222')
        
        url = reverse('search_patients') + '?phone=1711111111'
        
        response = authenticated_admin_client.get(url)
        
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert len(response.json()['data']) == 1
        assert response.json()['data'][0]['name'] == 'John Doe'
    
    def test_get_patient(self, authenticated_admin_client):
        patient = PatientFactory()
        url = reverse('get_patient', args=[patient.id])
        
        response = authenticated_admin_client.get(url)
        
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert response.json()['data']['name'] == patient.name