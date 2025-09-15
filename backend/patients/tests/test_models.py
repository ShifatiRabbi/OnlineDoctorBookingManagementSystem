import pytest
from tests.factories import PatientFactory

@pytest.mark.django_db
class TestPatientModel:
    def test_create_patient(self):
        patient = PatientFactory()
        assert patient.name is not None
        assert patient.phone is not None
        assert patient.gender in ['M', 'F', 'O']
    
    def test_patient_str_representation(self):
        patient = PatientFactory(name='John Doe')
        assert str(patient) == 'John Doe'