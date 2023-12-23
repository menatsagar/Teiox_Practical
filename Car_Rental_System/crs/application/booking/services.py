from django.db.models.manager import BaseManager
from crs.application.user.services import UserAppServices
from crs.application.vehicle.services import VehicleAppServices
from crs.domain.user.models import User
from crs.domain.vehicle.models import Vehicle
from crs.application.user.services import UserAppServices
from crs.domain.booking.models import Booking
from crs.domain.booking.services import BookingServices
from crs.utils.custom_exceptions import (
    BookingCreationException,
    EditBookingException,
    DeleteBookingException,
    BookingAlreadyExistsException
)


class BookingAppServices:
    """
    Application layer Services for Bookings.
    """

    def __init__(self) -> None:
        self.bookings_services = BookingServices()
        self.vehicles_services = VehicleAppServices()
        self.users_services = UserAppServices()
        

    def create_booking_from_dict(self, data: dict) -> Booking:
        """This method will return Booking."""

        user_id = data.get("user_id", None)
        vehicle_id = data.get("vehicle_id", None)
        booking_date = data.get("booking_date", None)
        purpose = data.get("purpose", None)
        total_hours = data.get("total_hours", None)
        booking_factory_method = (
            self.bookings_services.get_booking_factory()
        )
        try:
            exists_booking_obj = (
                self.bookings_services.get_booking_repo()
                .filter(vehicle__id=vehicle_id, booking_date=booking_date , is_active=True, mark_as_deleted=False)
                .exists()
            )
            
            if not exists_booking_obj:
               
                user = User.objects.get(id=user_id)
                vehicle = self.vehicles_services.list_vehicles().get(id=vehicle_id)
               
                booking_obj = booking_factory_method.build_entity_with_id(
                    booking_date=booking_date,
                    purpose=purpose,
                    vehicle=vehicle,
                    user=user,
                    total_hours=total_hours
                )
                booking_obj.save()
                return booking_obj
            raise BookingCreationException(
                "Vehicle is booked on for this date", f"{vehicle_id} this vehicle is booked"
            )
        except BookingCreationException as e:

            raise BookingCreationException(str(e), "Booking create exception")
        except Exception as e:
            
            raise BookingCreationException(
                "Booking already Exists", "Booking create exception"
            )

    def list_bookings(self, user: User) -> BaseManager[Booking]:
        """This method will return list of Bookings."""
        if not user.is_superuser:
            return self.bookings_services.get_booking_repo().filter(
                user__id=user.id,
                vehicle__is_active=True,
                is_active=True,
                mark_as_deleted = False
            )
        
        else:
            return (
                self.bookings_services.get_booking_repo()
                .filter(vehicle__is_active=True, user__is_active=True, is_active=True)
                .order_by("-created_at")
            )

    def get_booking_by_pk(self, pk: str, user: User) -> Booking:
        """This method will return Booking by pk."""
        try:
            return self.list_bookings(user=user).get(id=pk)
        except Exception as e:
            raise EditBookingException("Booking does not exist", str(e))

    def edit_booking_by_dict(self, pk: str, data: dict, user: User) -> Booking:
        booking_date = data.get("booking_date", None)
        purpose = data.get("purpose", None)
        try:
            booking = self.get_booking_by_pk(pk=pk, user=user)
            if booking:
                if booking_date and (
                    booking.booking_date != booking_date
                ):
                    booking.booking_date = booking_date
                if purpose and (booking.purpose != purpose):
                    booking.purpose = purpose
                booking.save()
                return booking
        except Exception as e:
            raise EditBookingException("Booking does not exist", str(e))

    def delete_booking_by_pk(self, pk: str, user: User) -> str:
        """This method will delete Booking."""
        try:
            booking = self.get_booking_by_pk(pk=pk, user=user)
            if booking:
                booking.mark_as_deleted = True
                booking.save()
                return booking
        except Exception as e:
            raise DeleteBookingException(
                "Booking does not exist or already deleted", str(e)
            )
