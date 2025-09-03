import pytest
from django.test import RequestFactory
from tests.factories import UserFactory, BranchFactory
from accounts.services import create_user_service, update_user_service, delete_user_service

@pytest.mark.django_db
class TestAccountsServices:
    def test_create_user_service(self):
        factory = RequestFactory()
        request = factory.post('/')
        branch = BranchFactory()
        
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'role': 'EMPLOYEE',
            'branch_id': branch.id
        }
        
        success, result = create_user_service(data, request)
        
        assert success is True
        assert result.username == 'testuser'
        assert result.role == 'EMPLOYEE'
    
    def test_create_user_service_missing_fields(self):
        factory = RequestFactory()
        request = factory.post('/')
        
        data = {
            'username': 'testuser',
            'email': 'test@example.com'
            # Missing password and role
        }
        
        success, result = create_user_service(data, request)
        
        assert success is False
        assert 'Missing required field' in result
    
    def test_update_user_service(self):
        factory = RequestFactory()
        request = factory.post('/')
        user = UserFactory()
        branch = BranchFactory()
        
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'branch_id': branch.id
        }
        
        success, result = update_user_service(user.id, data, request)
        
        assert success is True
        assert result.first_name == 'Updated'
        assert result.branch == branch
    
    def test_delete_user_service(self):
        factory = RequestFactory()
        request = factory.post('/')
        user = UserFactory()
        
        success, result = delete_user_service(user.id, request)
        
        assert success is True
        assert 'deleted successfully' in result