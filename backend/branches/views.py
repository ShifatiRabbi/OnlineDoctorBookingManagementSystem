from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.http import JsonResponse
from .services import create_branch_service, update_branch_service, delete_branch_service
from .models import Branch
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_branch(request):
    """
    API endpoint to create a new branch
    """
    try:
        data = json.loads(request.body)
        success, result = create_branch_service(data, request)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': 'Branch created successfully',
                'data': {
                    'id': result.id,
                    'name': result.name,
                    'slug': result.slug,
                    'address': result.address
                }
            }, status=201)
        else:
            return JsonResponse({
                'success': False,
                'error': result
            }, status=400)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_branch(request, branch_id):
    """
    API endpoint to update a branch
    """
    try:
        data = json.loads(request.body)
        success, result = update_branch_service(branch_id, data, request)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': 'Branch updated successfully',
                'data': {
                    'id': result.id,
                    'name': result.name,
                    'slug': result.slug,
                    'address': result.address
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'error': result
            }, status=400)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_branch(request, branch_id):
    """
    API endpoint to delete a branch
    """
    try:
        success, result = delete_branch_service(branch_id, request)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': result
            })
        else:
            return JsonResponse({
                'success': False,
                'error': result
            }, status=400)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_branches(request):
    """
    API endpoint to list all branches
    """
    try:
        branches = Branch.objects.all()
        branch_list = []
        
        for branch in branches:
            branch_list.append({
                'id': branch.id,
                'name': branch.name,
                'slug': branch.slug,
                'address': branch.address,
                'phones': branch.phones,
                'theme_config': branch.theme_config,
                'prescription_format': branch.prescription_format
            })
        
        return JsonResponse({
            'success': True,
            'data': branch_list
        })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)