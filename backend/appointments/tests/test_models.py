import pytest
from tests.factories import AppointmentFactory

@pytest.mark.django_db
class TestAppointmentModel:
    def test_create_appointment(self):
        appointment = AppointmentFactory()
        assert appointment.patient is not None
        assert appointment.doctor is not None
        assert appointment.branch is not None
        assert appointment.status in ['PENDING', 'CONFIRMED', 'CHECKED_IN', 'CANCELLED', 'COMPLETED']
    
    def test_appointment_str_representation(self):
        appointment = AppointmentFactory()
        assert str(appointment.patient) in str(appointment)
        assert str(appointment.doctor) in str(appointment)