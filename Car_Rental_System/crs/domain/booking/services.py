from django.db.models.manager import BaseManager
from crs.domain.booking.models import (
    Booking,
    BookingFactory,
)


class BookingServices:
    def get_booking_factory(
        self,
    ):
        return BookingFactory

    def get_booking_repo(self) -> BaseManager[Booking]:
        return Booking.objects
