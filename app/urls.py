from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewsetAPI,
    PassworedUpdateAPI,
    OrganizationViewSetAPI,
    MembershipsViewSetAPI
)

router = DefaultRouter()
router.register(r"sing-up",UserViewsetAPI,basename="sing up")
router.register(r"password",PassworedUpdateAPI,basename="passwored")
router.register(r"organization",OrganizationViewSetAPI,basename="organization")
router.register(r"memberships",MembershipsViewSetAPI,basename="memberships")

urlpatterns = [
    path("", include(router.urls)),
]