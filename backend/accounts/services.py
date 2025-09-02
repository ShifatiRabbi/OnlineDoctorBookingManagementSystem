from django.contrib.auth.hashers import make_password
from .models import User
from branches.models import Branch
from audit.models import AuditLog
import json

def create_user_service(data, request):
    """
    Service function to create a new user
    """
    try:
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'role']
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        # Check if username already exists
        if User.objects.filter(username=data['username']).exists():
            return False, "Username already exists"
        
        # Check if email already exists
        if User.objects.filter(email=data['email']).exists():
            return False, "Email already exists"
        
        # Validate role
        valid_roles = ['ADMIN', 'EMPLOYEE', 'DOCTOR']
        if data['role'] not in valid_roles:
            return False, "Invalid role"
        
        # Handle branch assignment
        branch = None
        if data.get('branch_id'):
            try:
                branch = Branch.objects.get(id=data['branch_id'])
            except Branch.DoesNotExist:
                return False, "Branch not found"
        
        # Create user
        user = User(
            username=data['username'],
            email=data['email'],
            password=make_password(data['password']),
            role=data['role'],
            branch=branch,
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            phone=data.get('phone', '')
        )
        user.save()
        
        # Create audit log
        AuditLog.objects.create(
            actor=request.user if request.user.is_authenticated else None,
            action="CREATE_USER",
            target_type="User",
            target_id=user.id,
            diff=data,
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return True, user
        
    except Exception as e:
        return False, str(e)

def update_user_service(user_id, data, request):
    """
    Service function to update a user
    """
    try:
        # Get user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return False, "User not found"
        
        # Check if username already exists (excluding current user)
        if 'username' in data and User.objects.filter(username=data['username']).exclude(id=user_id).exists():
            return False, "Username already exists"
        
        # Check if email already exists (excluding current user)
        if 'email' in data and User.objects.filter(email=data['email']).exclude(id=user_id).exists():
            return False, "Email already exists"
        
        # Handle branch assignment
        if 'branch_id' in data:
            if data['branch_id']:
                try:
                    branch = Branch.objects.get(id=data['branch_id'])
                    user.branch = branch
                except Branch.DoesNotExist:
                    return False, "Branch not found"
            else:
                user.branch = None
        
        # Update fields
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.password = make_password(data['password'])
        if 'role' in data:
            user.role = data['role']
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'is_active' in data:
            user.is_active = data['is_active']
        
        user.save()
        
        # Create audit log
        AuditLog.objects.create(
            actor=request.user if request.user.is_authenticated else None,
            action="UPDATE_USER",
            target_type="User",
            target_id=user.id,
            diff=data,
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return True, user
        
    except Exception as e:
        return False, str(e)

def delete_user_service(user_id, request):
    """
    Service function to delete a user
    """
    try:
        # Get user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return False, "User not found"
        
        # Create audit log before deletion
        AuditLog.objects.create(
            actor=request.user if request.user.is_authenticated else None,
            action="DELETE_USER",
            target_type="User",
            target_id=user.id,
            diff={"username": user.username, "email": user.email},
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        user.delete()
        
        return True, "User deleted successfully"
        
    except Exception as e:
        return False, str(e)