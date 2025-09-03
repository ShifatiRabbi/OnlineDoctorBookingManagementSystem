import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.http import JsonResponse
from .services import generate_daily_report_service, generate_monthly_report_service

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def daily_report(request):
    """
    API endpoint to generate daily report
    """
    try:
        date = request.GET.get('date')
        branch_id = request.GET.get('branch_id')
        
        if not date:
            return JsonResponse({
                'success': False,
                'error': 'Date parameter is required'
            }, status=400)
        
        success, result = generate_daily_report_service(date, branch_id)
        
        if success:
            return JsonResponse({
                'success': True,
                'data': result
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
def monthly_report(request):
    """
    API endpoint to generate monthly report
    """
    try:
        year = int(request.GET.get('year', datetime.now().year))
        month = int(request.GET.get('month', datetime.now().month))
        branch_id = request.GET.get('branch_id')
        
        success, result = generate_monthly_report_service(year, month, branch_id)
        
        if success:
            return JsonResponse({
                'success': True,
                'data': result
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