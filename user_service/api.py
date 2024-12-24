from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import F
from math import radians, cos, sin, sqrt, atan2
# from django.contrib.gis.geos import Point
# from django.contrib.gis.measure import D  # Distance
# from geopy.distance import geodesic
from user_service.models import Service, Customer
from user_service.serializers import ServiceSerializer, CustomerSerializer


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the distance between two lat/lon points using the Haversine formula."""
    R = 6371  # Earth's radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

@api_view(["POST"])
def search_services(request):
    """
    Search for services based on `service_name` and `distance`.
    """
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required."}, status=401)

    # Retrieve logged-in customer's details
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        return Response({"error": "Logged-in user is not a customer."}, status=400)

    # Extract `service_name` and `distance` from POST data
    service_name = request.data.get("service_name")
    distance = request.data.get("distance", 0)  # Default distance is 0 km

    if not service_name:
        return Response({"error": "Service name is required."}, status=400)

    if not distance or float(distance) <= 0:
        return Response({"error": "Distance must be a positive number."}, status=400)

    # Convert distance to float
    distance = float(distance)

    # Filter services by name and distance
    matching_services = []

    for service in Service.objects.filter(service_name__iexact=service_name):
        calculated_distance = calculate_distance(customer.latitude, customer.longitude, service.latitude, service.longitude)
        if calculated_distance <= distance:
            matching_services.append(service)

    # Serialize and return the results
    # services = Service.objects.all()
    service_data = ServiceSerializer(matching_services, many=True).data
    customer_data = CustomerSerializer(customer).data
    # service_data = ServiceSerializer(services, many=True).data

    return Response(
        {
            "customer": customer_data,
            "services": service_data,
        },
        status=200,
    )

