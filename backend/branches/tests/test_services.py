import pytest
import json
from django.urls import reverse
from tests.factories import BranchFactory

@pytest.mark.django_db
class TestBranchesViews:
    def test_create_branch(self, authenticated_admin_client):
        url = reverse('create_branch')
        data = {
            'name': 'Test Branch',
            'slug': 'test-branch',
            'address': '123 Test Street',
            'phones': '+8801712345678'
        }
        
        response = authenticated_admin_client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        assert response.json()['success'] is True
        assert response.json()['data']['name'] == 'Test Branch'
    
    def test_list_branches(self, authenticated_admin_client):
        BranchFactory.create_batch(3)
        url = reverse('list_branches')
        
        response = authenticated_admin_client.get(url)
        
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert len(response.json()['data']) >= 3
    
    def test_update_branch(self, authenticated_admin_client):
        branch = BranchFactory()
        url = reverse('update_branch', args=[branch.id])
        data = {
            'name': 'Updated Branch Name',
            'address': 'Updated Address'
        }
        
        response = authenticated_admin_client.put(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        assert response.json()['success'] is True
    
    def test_delete_branch(self, authenticated_admin_client):
        branch = BranchFactory()
        url = reverse('delete_branch', args=[branch.id])
        
        response = authenticated_admin_client.delete(url)
        
        assert response.status_code == 200
        assert response.json()['success'] is True