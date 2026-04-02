from django.contrib import admin
from django.urls import path, include
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Root endpoint - health check"""
    return Response({
        'status': 'ok',
        'message': 'Finance Backend API is running',
        'version': '1.0.0',
        'api_endpoints': {
            'api': '/api/v1/',
            'admin': '/admin/',
            'auth': '/api-auth/',
        }
    })

urlpatterns = [
    path('', health_check, name='health-check'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('finance.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
