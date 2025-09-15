from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.http import JsonResponse
from .services import get_audit_logs_service

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_audit_logs(request):
    """
    API endpoint to get audit logs
    """
    try:
        user_id = request.GET.get('user_id')
        action = request.GET.get('action')
        target_type = request.GET.get('target_type')
        limit = int(request.GET.get('limit', 100))
        
        success, result = get_audit_logs_service(user_id, action, target_type, limit)
        
        if success:
            log_list = []
            for log in result:
                log_list.append({
                    'id': log.id,
                    'actor': log.actor.username if log.actor else 'System',
                    'action': log.action,
                    'target_type': log.target_type,
                    'target_id': log.target_id,
                    'diff': log.diff,
                    'ip': log.ip,
                    'user_agent': log.user_agent,
                    'created_at': log.created_at
                })
            
            return JsonResponse({
                'success': True,
            'data': log_list
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