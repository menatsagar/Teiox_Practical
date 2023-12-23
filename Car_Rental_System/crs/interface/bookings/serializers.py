import datetime
from rest_framework import serializers
from crs.domain.booking.models import Booking
from crs.domain.vehicle.models import Vehicle
from crs.domain.user.models import User


class VehicleProfileSerializer(serializers.ModelSerializer):
    """VehicleProfile Serializer"""
   
    class Meta:
        model = Vehicle
        fields = [
            "registration_number",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    """UserProfile Serializer"""
   
    class Meta:
        model = User
        fields = [
            "email",
        ]

class BookingSerializer(serializers.ModelSerializer):
    """Booking serializer"""
    
    class Meta:
        model = Booking
        fields = [
            'id',
            'vehicle',
            'user',
            'booking_date',
            'purpose',
            'total_hours'
        ]
        
    def to_representation(self, instance):
        self.fields["vehicle"] = VehicleProfileSerializer(read_only=True)
        self.fields["user"] = UserProfileSerializer(read_only=True)
        return super(BookingSerializer, self).to_representation(instance)

class BookingCreateSerializer(serializers.Serializer):
    """Booking create serializer"""

    user_id = serializers.UUIDField(required=True)
    vehicle_id = serializers.UUIDField(required=True)
    booking_date = serializers.DateField(required=True)
    purpose = serializers.CharField(max_length=200, required=True)
    total_hours  = serializers.IntegerField(required = True)

    def validate_booking_date(self, value):
        today = datetime.date.today()
        if value < today:
            raise serializers.ValidationError("Invalid Date")
        return value

    def validate_purpose(self, value):
        if len(value) > 100:
            raise serializers.ValidationError(
                "purpose should not be more than 100 latter"
            )
        return value
    def validate_total_hours(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError(
                "total hours should be Integer value"
            )
        if value > 24 :
            raise serializers.ValidationError(
                "You can not book car for more than 24 hours"
            )
        return value

class BookingEditSerializer(serializers.Serializer):
    """Booking edit serializer"""

    booking_date = serializers.DateField(required=False)
    purpose = serializers.CharField(max_length=200, required=False)
    total_hours = serializers.IntegerField(required=True)

    def validate_booking_date(self, value):
        today = datetime.date.today()
        if value < today:
            raise serializers.ValidationError("Invalid Date")
        return value

    def validate_purpose(self, value):
        if len(value) > 100:
            raise serializers.ValidationError(
                "purpose should not be more than 100 latter"
            )
        
    def validate_total_hours(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError(
                "total hours should be Integer value"
            )
        
        if value > 24 :
            raise serializers.ValidationError(
                "You can not book car for more than 24 month"
            )
        return value
