import json
from datetime import datetime, timedelta

def assert_response_success(response, status_code=200):
    """Assert that API response is successful"""
    assert response.status_code == status_code
    assert response.json()['success'] is True

def assert_response_error(response, status_code=400):
    """Assert that API response has error"""
    assert response.status_code == status_code
    assert response.json()['success'] is False

def create_test_appointment_data(patient, doctor, branch):
    """Create test appointment data"""
    tomorrow = datetime.now().date() + timedelta(days=1)
    return {
        'patient_id': patient.id,
        'doctor_id': doctor.id,
        'branch_id': branch.id,
        'date': tomorrow.strftime('%Y-%m-%d'),
        'time': '09:00:00'
    }