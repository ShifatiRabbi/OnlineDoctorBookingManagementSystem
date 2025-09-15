from .models import SMSMessage
from audit.models import AuditLog
import json

def send_sms_service(data, request):
    """
    Service function to send SMS
    """
    try:
        # Validate required fields
        required_fields = ['to', 'content', 'type']
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        # Create SMS record
        sms = SMSMessage(
            to=data['to'],
            content=data['content'],
            type=data['type'],
            status='PENDING'
        )
        sms.save()
        
        # Here you would integrate with your SMS provider
        # For now, we'll just mark it as sent
        sms.status = 'SENT'
        sms.provider_id = 'SIMULATED'
        sms.save()
        
        # Create audit log
        AuditLog.objects.create(
            actor=request.user if request.user.is_authenticated else None,
            action="SEND_SMS",
            target_type="SMSMessage",
            target_id=sms.id,
            diff=data,
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return True, sms
        
    except Exception as e:
        return False, str(e)

def get_sms_history_service(phone=None, type=None, limit=100):
    """
    Service function to get SMS history
    """
    try:
        sms_messages = SMSMessage.objects.all().order_by('-created_at')
        
        if phone:
            sms_messages = sms_messages.filter(to=phone)
        
        if type:
            sms_messages = sms_messages.filter(type=type)
        
        if limit:
            sms_messages = sms_messages[:limit]
        
        return True, sms_messages
        
    except Exception as e:
        return False, str(e)