from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewsetAPI,
    PassworedUpdateAPI,
    OrganizationViewSetAPI,
    MembershipsViewSetAPI,
    ProjectViewSetAPI
)

router = DefaultRouter()
router.register(r"sing-up",UserViewsetAPI,basename="sing up")
router.register(r"password",PassworedUpdateAPI,basename="passwored")
router.register(r"organization",OrganizationViewSetAPI,basename="organization")
router.register(r"memberships",MembershipsViewSetAPI,basename="memberships")
router.register(r"project",ProjectViewSetAPI,basename="project")

urlpatterns = [
    path("", include(router.urls)),
]