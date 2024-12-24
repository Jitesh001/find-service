from rest_framework import serializers
from core.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'mobile', 'first_name', 'last_name', 'is_email_verified']


class LocationUpdateSerializer(serializers.Serializer):
    latitude = serializers.FloatField(required=True, min_value=-90.0, max_value=90.0)
    longitude = serializers.FloatField(required=True, min_value=-180.0, max_value=180.0)

    def validate(self, data):
        if not (-90.0 <= data['latitude'] <= 90.0):
            raise serializers.ValidationError("Invalid latitude value.")
        if not (-180.0 <= data['longitude'] <= 180.0):
            raise serializers.ValidationError("Invalid longitude value.")
        return data
