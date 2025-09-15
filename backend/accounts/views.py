from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.http import JsonResponse
from .services import create_user_service, update_user_service, delete_user_service
from .models import User
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_user(request):
    """
    API endpoint to create a new user
    """
    try:
        data = json.loads(request.body)
        success, result = create_user_service(data, request)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': 'User created successfully',
                'data': {
                    'id': result.id,
                    'username': result.username,
                    'email': result.email,
                    'role': result.role,
                    'branch': result.branch.id if result.branch else None
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
def update_user(request, user_id):
    """
    API endpoint to update a user
    """
    try:
        data = json.loads(request.body)
        success, result = update_user_service(user_id, data, request)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': 'User updated successfully',
                'data': {
                    'id': result.id,
                    'username': result.username,
                    'email': result.email,
                    'role': result.role,
                    'branch': result.branch.id if result.branch else None,
                    'is_active': result.is_active
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
def delete_user(request, user_id):
    """
    API endpoint to delete a user
    """
    try:
        success, result = delete_user_service(user_id, request)
        
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
@permission_classes([IsAuthenticated, IsAdminUser])
def list_users(request):
    """
    API endpoint to list all users
    """
    try:
        users = User.objects.all()
        user_list = []
        
        for user in users:
            user_list.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'branch': user.branch.id if user.branch else None,
                'branch_name': user.branch.name if user.branch else None,
                'phone': user.phone,
                'is_active': user.is_active,
                'last_login': user.last_login
            })
        
        return JsonResponse({
            'success': True,
            'data': user_list
        })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)