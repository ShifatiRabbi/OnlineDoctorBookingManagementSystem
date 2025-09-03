import pytest
from tests.factories import AppointmentFactory
from prescriptions.models import Prescription, Medicine, Test

@pytest.mark.django_db
class TestPrescriptionModel:
    def test_create_medicine(self):
        medicine = Medicine.objects.create(
            name='Test Medicine',
            generic='Test Generic',
            strength='500mg',
            form='TAB'
        )
        assert medicine.name == 'Test Medicine'
        assert medicine.form == 'TAB'
    
    def test_create_test(self):
        test = Test.objects.create(
            name='Blood Test',
            category='BLOOD'
        )
        assert test.name == 'Blood Test'
        assert test.category == 'BLOOD'