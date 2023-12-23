from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from crs.application.booking.services import BookingAppServices
from crs.domain.booking.models import Booking
from crs.utils.pagination import Pagination
from crs.utils.user_permissions import IsSuperUser, IsStaff
from .serializers import (
    BookingSerializer,
    BookingCreateSerializer,
    BookingEditSerializer,
)
from crs.utils.custom_exceptions import (
    BookingCreationException,
    EditBookingException,
    DeleteBookingException,
)

from crs.utils.custom_response import CustomResponse


class BookingViewSet(viewsets.ViewSet):
   

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = Pagination

    bookings_app_services = BookingAppServices()

    def get_serializer_class(self):
        if self.action == "add":
            return BookingCreateSerializer
        if self.action == "all":
            return BookingSerializer
        if self.action == "get":
            return BookingSerializer
        if self.action == "delete":
            return BookingSerializer
        return BookingEditSerializer

    @action(detail=False, methods=["post"], name="add")
    def add(self, request):
        """This method will create Booking by dict"""

        serializer = self.get_serializer_class()
        serializer_obj = serializer(data=request.data)
        if serializer_obj.is_valid():
           
            try:
                booking_obj = (
                    self.bookings_app_services.create_booking_from_dict(
                        data=serializer_obj.data
                    )
                )
                response = BookingSerializer(booking_obj)
                return CustomResponse(
                    data=response.data,
                    message="You have created booking successfully",
                )
            except BookingCreationException as e:
                return CustomResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message=e.item,
                )
        return CustomResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=serializer_obj.errors,
        )

    @action(detail=False, methods=["get"], name="all")
    def all(self, request):
        """This method will return list of Bookings"""
        serializer = self.get_serializer_class()
        queryset = self.bookings_app_services.list_bookings(
            user=self.request.user
        )
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer_obj = serializer(paginated_queryset, many=True)
        paginated_data = paginator.get_paginated_response(serializer_obj.data).data
        message = "Successfully listed all bookings."
        return CustomResponse(data=paginated_data, message=message)

    @action(detail=True, methods=["get"], name="get")
    def get(self, request, pk=None):
        """This method will get Booking by pk"""
        get_serializer = self.get_serializer_class()
        try:
            booking_obj = self.bookings_app_services.get_booking_by_pk(
                pk=pk, user=self.request.user
            )
            response = get_serializer(booking_obj)
            return CustomResponse(
                data=response.data, message="Successfully get booking."
            )
        except EditBookingException as e:
            return CustomResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=e.item,
            )

    @action(detail=True, methods=["patch"], name="edit")
    def edit(self, request, pk=None):
        """This method will edit Booking by pk"""
        serializer = self.get_serializer_class()
        serializer_obj = serializer(data=request.data)
        if serializer_obj.is_valid():
            try:
                booking_obj = (
                    self.bookings_app_services.edit_booking_by_dict(
                        data=serializer_obj.data, user=self.request.user, pk=pk
                    )
                )
                booking = BookingSerializer(booking_obj)
                return CustomResponse(
                    data=booking.data,
                    message="You have updated booking successfully",
                )
            except EditBookingException as e:
                return CustomResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message=e.item,
                )
        return CustomResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=serializer_obj.errors,
        )

    @action(detail=True, methods=["delete"], name="delete")
    def delete(self, request, pk=None):
        """This method will delete Booking by pk"""
        try:
            booking_obj = self.bookings_app_services.delete_booking_by_pk(
                pk=pk, user=self.request.user
            )
            response = BookingSerializer(booking_obj)
            return CustomResponse(
                data=response.data, message="You have deleted successfully"
            )
        except DeleteBookingException as e:
            return CustomResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=e.item,
            )
