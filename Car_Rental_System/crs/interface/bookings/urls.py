from .views import BookingViewSet

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"booking", BookingViewSet, basename="booking")