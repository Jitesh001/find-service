from django.urls import path
from core.views import LoginView, LogoutView, UpdateLocationView, CustomerSignupView, ServiceSignupView

urlpatterns = [
    path('signup/customer/', CustomerSignupView.as_view(), name='customer_signup'),
    path('signup/service/', ServiceSignupView.as_view(), name='service_signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update-location/', UpdateLocationView.as_view(), name='update_location'),
]
