import pytest
import json
from django.urls import reverse
from tests.factories import UserFactory, BranchFactory

@pytest.mark.django_db
class TestAccountsViews:
    def test_create_user_as_admin(self, authenticated_admin_client):
        branch = BranchFactory()
        url = reverse('create_user')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'role': 'EMPLOYEE',
            'branch_id': branch.id
        }
        
        response = authenticated_admin_client.post(
            url, 
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        assert response.json()['success'] is True
        assert response.json()['data']['username'] == 'newuser'
    
    def test_create_user_unauthorized(self, api_client):
        url = reverse('create_user')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'role': 'EMPLOYEE'
        }
        
        response = api_client.post(
            url, 
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 403
    
    def test_list_users(self, authenticated_admin_client):
        UserFactory.create_batch(3)
        url = reverse('list_users')
        
        response = authenticated_admin_client.get(url)
        
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert len(response.json()['data']) >= 3
    
    def test_update_user(self, authenticated_admin_client):
        user = UserFactory()
        branch = BranchFactory()
        url = reverse('update_user', args=[user.id])
        data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'branch_id': branch.id
        }
        
        response = authenticated_admin_client.put(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        assert response.json()['success'] is True
    
    def test_delete_user(self, authenticated_admin_client):
        user = UserFactory()
        url = reverse('delete_user', args=[user.id])
        
        response = authenticated_admin_client.delete(url)
        
        assert response.status_code == 200
        assert response.json()['success'] is True