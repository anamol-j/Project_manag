from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewsetAPI,
    PassworedUpdateAPI
)

router = DefaultRouter()
router.register(r"sing-up",UserViewsetAPI,basename="sing up")
router.register(r"password",PassworedUpdateAPI,basename="passwored")


urlpatterns = [
    path("", include(router.urls)),
]