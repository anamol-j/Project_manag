from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewsetAPI

router = DefaultRouter()
router.register(r"sing-up",UserViewsetAPI,basename="sing up")

urlpatterns = [
    path("", include(router.urls)),
]