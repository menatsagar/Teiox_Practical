"""This is a model module to store Vehicle data in to the database"""

import uuid
from dataclasses import dataclass
from django.db import models
from crs.utils.base_models import AuditModelMixin


@dataclass(frozen=True)
class VehicleID:
    value: uuid.UUID

class Vehicle(AuditModelMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    model = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=50)
    transmission = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=20, null=True, blank=True)
    registration_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.model}"

    class Meta:
        db_table = "vehicle"


class VehicleFactory:
    @staticmethod
    def build_entity(
        id: VehicleID,
        model: str,
        fuel_type: str,
        transmission: str,
        color: str,
        registration_number: str,
       
    ) -> Vehicle:
        return Vehicle(
            id=id.value,
            model=model,
            fuel_type=fuel_type,
            transmission=transmission,
            color=color,
            registration_number = registration_number
        )

    @classmethod
    def build_entity_with_id(
        cls,
        model: str,
        fuel_type: str,
        transmission: str,
        color: str,
        registration_number: str,
    ) -> Vehicle:
        entity_id = VehicleID(uuid.uuid4())
        return cls.build_entity(
            id=entity_id,
            model=model,
            fuel_type=fuel_type,
            transmission=transmission,
            color=color,
            registration_number = registration_number
        )

    @classmethod
    def update_entity(
        self,
        vehicle: Vehicle,
        model: str,
        fuel_type: str,
        transmission: str,
        color: str,
        registration_number: str,
    ) -> Vehicle:
        if model:
            vehicle.model = model
        if fuel_type:
            vehicle.fuel_type = fuel_type
        if transmission:
            vehicle.transmission = transmission
        if color:
            vehicle.color = color

        if registration_number:
            vehicle.registration_number = registration_number
        return vehicle
