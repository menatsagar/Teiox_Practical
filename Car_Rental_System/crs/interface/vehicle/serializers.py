import re, datetime
from django.conf import settings
from rest_framework import serializers
from crs.domain.vehicle.models import Vehicle
from crs.domain.user.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    """UserProfile Serializer"""

    class Meta:
        model = User
        fields = [
            "username",
        ]


class VehicleSerializer(serializers.ModelSerializer):
    """Vehicle Serializer"""
    class Meta:
        model = Vehicle
        fields = [
            "id",
            "model",
            "fuel_type",
            "transmission",
            "color",
            "registration_number",
            
        ]

    def to_representation(self, instance):
        return super(VehicleSerializer, self).to_representation(instance)

class VehicleCreateSerializer(serializers.Serializer):
    """Vehicle create serializer"""


    model = serializers.CharField(max_length=50, required=True)
    fuel_type = serializers.CharField(max_length=50, required=True)
    transmission = serializers.CharField(max_length=50)
    color = serializers.CharField(max_length=20)
    registration_number = serializers.CharField(max_length=20)

class VehicleEditSerializer(serializers.Serializer):
    """Vehicle edit serializer"""

    model = serializers.CharField(max_length=50, required=True)
    fuel_type = serializers.CharField(max_length=50, required=True)
    transmission = serializers.CharField(max_length=50)
    color = serializers.CharField(max_length=20)
    registration_number = serializers.CharField(max_length=20)
