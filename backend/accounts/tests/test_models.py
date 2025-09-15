import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from tests.factories import UserFactory, AdminUserFactory, DoctorUserFactory

User = get_user_model()

@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = UserFactory()
        assert user.username is not None
        assert user.email is not None
        assert user.role == 'EMPLOYEE'
        assert user.check_password('testpass123')
    
    def test_create_admin_user(self):
        admin = AdminUserFactory()
        assert admin.role == 'ADMIN'
        assert admin.is_staff is True
        assert admin.is_superuser is True
    
    def test_create_doctor_user(self):
        doctor = DoctorUserFactory()
        assert doctor.role == 'DOCTOR'
    
    def test_user_str_representation(self):
        user = UserFactory(username='testuser')
        assert str(user) == 'testuser (EMPLOYEE)'