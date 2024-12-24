from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from core.models import User
from user_service.models import Customer, Service
from django.shortcuts import render
from .serializers import LocationUpdateSerializer, UserSerializer
from rest_framework.serializers import Serializer, CharField, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.middleware.csrf import get_token
from django.http import JsonResponse

def csrf_token_view(request):
    csrf_token = get_token(request)
    response = JsonResponse({"csrfToken": csrf_token})
    response["Access-Control-Allow-Origin"] = "http://localhost:3000"  
    response["Access-Control-Allow-Credentials"] = "true" 
    return response

def homepage(request):
    return render(request, "frontend/index.html")

# Serializer for Customer Signup
class CustomerSignupSerializer(Serializer):
    email = CharField(required=True)
    mobile = CharField(required=True)
    password1 = CharField(write_only=True)
    password2 = CharField(write_only=True)
    first_name = CharField(required=True)
    last_name = CharField(required=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise ValidationError({"password2": "Passwords do not match."})
        return data


# Serializer for Service Signup
class ServiceSignupSerializer(CustomerSignupSerializer):
    service_name = CharField(required=True)


# Customer Signup API
class CustomerSignupView(APIView):
    def post(self, request):
        serializer = CustomerSignupSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = User.objects.create_user(
                email=data['email'],
                username=data['email'],
                password=data['password1'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                mobile=data['mobile'],
            )
            Customer.objects.create(user=user)
            return Response({"message": "Customer registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Service Signup API
class ServiceSignupView(APIView):
    def post(self, request):
        serializer = ServiceSignupSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = User.objects.create_user(
                email=data['email'],
                username=data['email'],
                password=data['password1'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                mobile=data['mobile'],
            )
            Service.objects.create(user=user, service_name=data['service_name'])
            return Response({"message": "Service provider registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            login(request, user)
            user_type = 'customer' if hasattr(user, 'customer') else 'service'
            csrf_token = get_token(request)
            return Response({'message': 'Login successful', 'user_type': user_type, "csrfToken": csrf_token}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


class UpdateLocationView(APIView):
    authentication_classes = [SessionAuthentication]  # Add TokenAuthentication if needed
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LocationUpdateSerializer(data=request.data)
        if serializer.is_valid():
            latitude = serializer.validated_data['latitude']
            longitude = serializer.validated_data['longitude']
            user = request.user

            # Update location for Customer or Service user
            if hasattr(user, 'customer'):
                user.customer.latitude = latitude
                user.customer.longitude = longitude
                user.customer.save()
            elif hasattr(user, 'service'):
                user.service.latitude = latitude
                user.service.longitude = longitude
                user.service.save()
            else:
                return Response({'error': 'User type not recognized'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'Location updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
