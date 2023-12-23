from crs.interface.user.views import UserViewSet, UserLogoutViewset, UserBookingsViewSet
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r"user", UserViewSet, basename="user")
# router.register(r"", UserRegistrationView, basename="registration")
# router.register(r"", UserLoginView, basename="login")
router.register(r"user", UserLogoutViewset, basename="logout")
router.register(r"user", UserBookingsViewSet, basename="user_bookings")
