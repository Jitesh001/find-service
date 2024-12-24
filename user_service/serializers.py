from rest_framework import serializers
from user_service.models import Customer, Service

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user', 'latitude', 'longitude']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['user', 'service_name', 'latitude', 'longitude']
