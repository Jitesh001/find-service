from rest_framework.views import APIView
from rest_framework.response import Response
from user_service.models import Customer, Service
from user_service.serializers import CustomerSerializer, ServiceSerializer

class ServiceListView(APIView):
    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

class CustomerListView(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
