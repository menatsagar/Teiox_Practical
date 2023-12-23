from django.db.models.manager import BaseManager
from crs.domain.vehicle.models import Vehicle, VehicleFactory

class VehicleServices:
    def get_vehicle_factory(
        self,
    ):
        return VehicleFactory

    def get_vehicle_repo(self) -> BaseManager[Vehicle]:
        return Vehicle.objects
