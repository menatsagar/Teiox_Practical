from rest_framework import serializers
from crs.domain.user.models import User


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=254, required=True)
    password = serializers.CharField(max_length=254, required=True)


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email","password"]

class UserBookingsSerializer(serializers.ModelSerializer):
    bookings = serializers.SerializerMethodField()
    def get_bookings(self, obj):
        return obj.user_bookings.all()
    class Meta:
        model = User
        fields = [ "email", "bookings"]