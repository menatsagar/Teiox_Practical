from .views import VehicleViewSet

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"vehicle", VehicleViewSet, basename="vehicle")
