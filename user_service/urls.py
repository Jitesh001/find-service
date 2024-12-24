# user_service/urls.py

from django.urls import path
from .views import ServiceListView, CustomerListView

urlpatterns = [
    path('services/', ServiceListView.as_view(), name='services_list'),
    path('customers/', CustomerListView.as_view(), name='customers_list'),
]
