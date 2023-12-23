from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action

from .serializers import (
    VehicleSerializer,
    VehicleCreateSerializer,
    VehicleEditSerializer,
)
from crs.application.vehicle.services import VehicleAppServices
from crs.utils.user_permissions import  IsStaff, IsSuperUser
from crs.utils.custom_exceptions import (
    VehicleCreationException,
    EditVehicleException,
    DeleteVehicleException,
)

from crs.utils.pagination import Pagination
from crs.utils.custom_response import CustomResponse


class VehicleViewSet(viewsets.ViewSet):
    """VehicleViewSet for create, update, delete and list Vehicles"""

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, (IsSuperUser | IsStaff))
    pagination_class = Pagination

    vehicles_app_services = VehicleAppServices()

    def get_serializer_class(self):
        if self.action == "add":
            return VehicleCreateSerializer
        if self.action == "all":
            return VehicleSerializer
        if self.action == "get":
            return VehicleSerializer
        if self.action == "delete":
            return VehicleSerializer
        return VehicleEditSerializer

    @action(detail=False, methods=["post"], name="add")
    def add(self, request):
        """This method will create Vehicle by dict"""

        serializer = self.get_serializer_class()
        serializer_obj = serializer(data=request.data)

        if serializer_obj.is_valid():
            try:
                vehicle_obj = self.vehicles_app_services.create_vehicle_from_dict(
                    data=serializer_obj.data
                )
                if vehicle_obj:
                    response = VehicleSerializer(vehicle_obj)
                    return CustomResponse(
                        data=response.data,
                        message="You have created vehicle successfully",
                    )
            except VehicleCreationException as e:
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
        serializer = self.get_serializer_class()
        queryset = self.vehicles_app_services.list_vehicles()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer_obj = serializer(paginated_queryset, many=True)
        paginated_data = paginator.get_paginated_response(serializer_obj.data).data
        message = "Successfully listed all vehicles."
        return CustomResponse(data=paginated_data, message=message)

    @action(detail=True, methods=["get"], name="get")
    def get(self, request, pk=None):
        """This method will get vehicle by pk"""
        get_serializer = self.get_serializer_class()
        try:
            vehicle_obj = self.vehicles_app_services.get_vehicle_by_pk(pk=pk)
            response = get_serializer(vehicle_obj)
            return CustomResponse(
                data=response.data, message="Successfully get vehicle."
            )
        except EditVehicleException as e:
            return CustomResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=e.item,
            )

    @action(detail=True, methods=["patch"], name="edit")
    def edit(self, request, pk=None):
        serializer = self.get_serializer_class()
        serializer_obj = serializer(data=request.data)
        if serializer_obj.is_valid():
            try:
                vehicle_obj = self.vehicles_app_services.edit_vehicle_by_dict(
                    data=serializer_obj.data, pk=pk
                )
                vehicle = VehicleSerializer(vehicle_obj)
                return CustomResponse(
                    data=vehicle.data, message="You have Edited vehicle data successfully"
                )
            except EditVehicleException as e:
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
        """This method will delete Vehicle by pk"""
        try:
            vehicle_obj = self.vehicles_app_services.delete_vehicle_by_pk(pk=pk)
            response = VehicleSerializer(vehicle_obj)
            return CustomResponse(
                data=response.data, message="You have deleted successfully"
            )
        except DeleteVehicleException as e:
            return CustomResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=e.item,
            )
