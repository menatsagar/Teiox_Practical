"""This is a model module to store Booking data in to the database"""

import uuid

from dataclasses import dataclass
from django.db import models

from crs.domain.user.models import User
from crs.domain.vehicle.models import Vehicle

from crs.utils.base_models import AuditModelMixin


@dataclass(frozen=True)
class BookingID:
    """
    This is a value object that should be used to generate and pass the
    BookingID to the BookingFactory
    """

    value: uuid.UUID


# ----------------------------------------------------------------------
# Booking Model
# ----------------------------------------------------------------------


class Booking(AuditModelMixin):
    """This model stores the data into Booking table in db"""

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "user_bookings")
    booking_date = models.DateField()
    purpose = models.CharField(max_length=300)
    total_hours = models.IntegerField()

    def __str__(self):
        return self.user.email +" - "+ self.vehicle.registration_number

    class Meta:
        db_table = "booking"


class BookingFactory:
    """This is a factory method used for build an instance of Booking"""

    @staticmethod
    def build_entity_with_id(
        vehicle: Vehicle, user: User, booking_date: str, purpose: str, total_hours:int
    ) -> Booking:
        return Booking(
            id=BookingID(uuid.uuid4()).value,
            vehicle=vehicle,
            user=user,
            booking_date=booking_date,
            purpose=purpose,
            total_hours = total_hours
        )
