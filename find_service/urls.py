from django.contrib import admin
from django.urls import path, include
from core.views import homepage, csrf_token_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user_service.urls')),  # Include user_service URLs
    path('api/', include('core.urls')),
    path("", homepage, name="homepage"), 
    path('api/csrf-token/',csrf_token_view, name="csrf_token_view" ),   
]
