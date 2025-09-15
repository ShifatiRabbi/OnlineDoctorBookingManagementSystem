from .models import Branch
from audit.models import AuditLog
import json

def create_branch_service(data, request):
    """
    Service function to create a new branch
    """
    try:
        # Validate required fields
        required_fields = ['name', 'slug', 'address']
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        # Check if slug already exists
        if Branch.objects.filter(slug=data['slug']).exists():
            return False, "Slug already exists"
        
        # Create branch
        branch = Branch(
            name=data['name'],
            slug=data['slug'],
            address=data['address'],
            phones=data.get('phones', ''),
            theme_config=data.get('theme_config', {}),
            prescription_format=data.get('prescription_format', {})
        )
        branch.save()
        
        # Create audit log
        AuditLog.objects.create(
            actor=request.user if request.user.is_authenticated else None,
            action="CREATE_BRANCH",
            target_type="Branch",
            target_id=branch.id,
            diff=data,
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return True, branch
        
    except Exception as e:
        return False, str(e)

def update_branch_service(branch_id, data, request):
    """
    Service function to update a branch
    """
    try:
        # Get branch
        try:
            branch = Branch.objects.get(id=branch_id)
        except Branch.DoesNotExist:
            return False, "Branch not found"
        
        # Check if slug already exists (excluding current branch)
        if 'slug' in data and Branch.objects.filter(slug=data['slug']).exclude(id=branch_id).exists():
            return False, "Slug already exists"
        
        # Update fields
        if 'name' in data:
            branch.name = data['name']
        if 'slug' in data:
            branch.slug = data['slug']
        if 'address' in data:
            branch.address = data['address']
        if 'phones' in data:
            branch.phones = data['phones']
        if 'theme_config' in data:
            branch.theme_config = data['theme_config']
        if 'prescription_format' in data:
            branch.prescription_format = data['prescription_format']
        
        branch.save()
        
        # Create audit log
        AuditLog.objects.create(
            actor=request.user if request.user.is_authenticated else None,
            action="UPDATE_BRANCH",
            target_type="Branch",
            target_id=branch.id,
            diff=data,
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return True, branch
        
    except Exception as e:
        return False, str(e)

def delete_branch_service(branch_id, request):
    """
    Service function to delete a branch
    """
    try:
        # Get branch
        try:
            branch = Branch.objects.get(id=branch_id)
        except Branch.DoesNotExist:
            return False, "Branch not found"
        
        # Create audit log before deletion
        AuditLog.objects.create(
            actor=request.user if request.user.is_authenticated else None,
            action="DELETE_BRANCH",
            target_type="Branch",
            target_id=branch.id,
            diff={"name": branch.name, "slug": branch.slug},
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        branch.delete()
        
        return True, "Branch deleted successfully"
        
    except Exception as e:
        return False, str(e)