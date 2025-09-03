from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.http import JsonResponse
from .services import send_sms_service, get_sms_history_service
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def send_sms(request):
    """
    API endpoint to send SMS
    """
    try:
        data = json.loads(request.body)
        success, result = send_sms_service(data, request)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': 'SMS sent successfully',
                'data': {
                    'id': result.id,
                    'to': result.to,
                    'content': result.content,
                    'type': result.type,
                    'status': result.status
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

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_sms_history(request):
    """
    API endpoint to get SMS history
    """
    try:
        phone = request.GET.get('phone')
        sms_type = request.GET.get('type')
        limit = int(request.GET.get('limit', 100))
        
        success, result = get_sms_history_service(phone, sms_type, limit)
        
        if success:
            sms_list = []
            for sms in result:
                sms_list.append({
                    'id': sms.id,
                    'to': sms.to,
                    'content': sms.content,
                    'type': sms.type,
                    'status': sms.status,
                    'provider_id': sms.provider_id,
                    'error': sms.error,
                    'created_at': sms.created_at
                })
            
            return JsonResponse({
                'success': True,
                'data': sms_list
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