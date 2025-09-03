import pytest
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user(db):
    return User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='testpass123',
        role='ADMIN',
        is_staff=True,
        is_superuser=True
    )

@pytest.fixture
def employee_user(db):
    return User.objects.create_user(
        username='employee',
        email='employee@example.com',
        password='testpass123',
        role='EMPLOYEE'
    )

@pytest.fixture
def doctor_user(db):
    return User.objects.create_user(
        username='doctor',
        email='doctor@example.com',
        password='testpass123',
        role='DOCTOR'
    )

@pytest.fixture
def request_factory():
    return RequestFactory()

@pytest.fixture
def authenticated_admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client

@pytest.fixture
def authenticated_employee_client(api_client, employee_user):
    api_client.force_authenticate(user=employee_user)
    return api_client

@pytest.fixture
def authenticated_doctor_client(api_client, doctor_user):
    api_client.force_authenticate(user=doctor_user)
    return api_client