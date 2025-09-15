from .models import AuditLog
from accounts.models import User

def get_audit_logs_service(user_id=None, action=None, target_type=None, limit=100):
    """
    Service function to get audit logs
    """
    try:
        audit_logs = AuditLog.objects.all().order_by('-created_at')
        
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                audit_logs = audit_logs.filter(actor=user)
            except User.DoesNotExist:
                pass
        
        if action:
            audit_logs = audit_logs.filter(action=action)
        
        if target_type:
            audit_logs = audit_logs.filter(target_type=target_type)
        
        if limit:
            audit_logs = audit_logs[:limit]
        
        return True, audit_logs
        
    except Exception as e:
        return False, str(e)