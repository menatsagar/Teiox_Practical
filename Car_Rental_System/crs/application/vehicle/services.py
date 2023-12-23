from django.db.models.manager import BaseManager
from crs.domain.user.models import UserPersonalData
from crs.domain.user.services import UserServices
from crs.domain.vehicle.models import Vehicle
from crs.domain.vehicle.services import VehicleServices
from django.db import transaction
from crs.utils.custom_exceptions import (
    VehicleCreationException,
    EditVehicleException,
    DeleteVehicleException,
)


class VehicleAppServices:
    """
    Application layer Services for Vehicles.
    """

    def __init__(self) -> None:
        self.vehicles_services = VehicleServices()
        self.user_services = UserServices()

    def create_vehicle_from_dict(self, data: dict) -> Vehicle:
        model = data.get("model", None)
        fuel_type = data.get("fuel_type", None)
        transmission = data.get("transmission", None)
        color = data.get("color", None)
        registration_number = data.get("registration_number", None)
        vehicle_factory_method = self.vehicles_services.get_vehicle_factory()
        try:
            with transaction.atomic():
                exist_vehicle_obj = self.vehicles_services.get_vehicle_repo().filter(registration_number=registration_number)
                if exist_vehicle_obj:
                    raise VehicleCreationException(f"{registration_number}", "already exists")
               

                vehicle_obj = vehicle_factory_method.build_entity_with_id(
                    model=model,
                    fuel_type= fuel_type,
                    transmission= transmission,
                    color=color,
                    registration_number=registration_number
                )
                vehicle_obj.save()
                return vehicle_obj
        except VehicleCreationException as e:
            raise VehicleCreationException(str(e), "Vehicle create exception")

    def list_vehicles(self) -> BaseManager[Vehicle]:
        """This method will return list of Vehicles."""
        return (
            self.vehicles_services.get_vehicle_repo()
            .filter(is_active=True)
            .order_by("-created_at")
        )

    def get_vehicle_by_pk(self, pk: str):
        try:
            return self.list_vehicles().get(id=pk)
        except Exception as e:
          
            raise EditVehicleException("Vehicle does not exist", str(e))

    def edit_vehicle_by_dict(self, pk, data: dict) -> Vehicle:
       
       
        model = data.get("model", None)
        fuel_type = data.get("fuel_type", None)
        transmission = data.get("transmission", None)
        color = data.get("color", None)
        registration_number = data.get("registration_number", None)
        vehicle_factory_method = self.vehicles_services.get_vehicle_factory()
        try:
            vehicle_obj = self.get_vehicle_by_pk(pk=pk)
          
            vehicle = vehicle_factory_method.update_entity(
                vehicle=vehicle_obj,
                model=model,
                fuel_type=fuel_type,
                transmission=transmission,
                color=color,
                registration_number=registration_number,
            )
            
            vehicle.save()
            return vehicle
        except Exception as e:
           
            raise EditVehicleException("Vehicle does not exist", str(e))

    def delete_vehicle_by_pk(self, pk: str) -> str:
        """This method will delete Vehicle."""
        try:
            with transaction.atomic():
                vehicle = self.get_vehicle_by_pk(pk=pk)
                vehicle.mark_as_deleted = True
                vehicle.save()
                return vehicle
        except Exception as e:
            raise DeleteVehicleException(
                "Vehicle does not exist or already deleted", str(e)
            )
