import pytest
from tests.factories import DoctorFactory, SpecialtyFactory

@pytest.mark.django_db
class TestDoctorModel:
    def test_create_doctor(self):
        doctor = DoctorFactory()
        assert doctor.user.role == 'DOCTOR'
        assert doctor.degrees is not None
        assert doctor.fee > 0
        assert doctor.active is True
    
    def test_doctor_str_representation(self):
        doctor = DoctorFactory()
        assert 'Dr.' in str(doctor)
    
    def test_doctor_specialties(self):
        specialty1 = SpecialtyFactory()
        specialty2 = SpecialtyFactory()
        doctor = DoctorFactory(specialties=[specialty1, specialty2])
        
        assert doctor.specialties.count() == 2
        assert specialty1 in doctor.specialties.all()
        assert specialty2 in doctor.specialties.all()