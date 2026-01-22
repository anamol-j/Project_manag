from .models import Membership
from rest_framework.permissions import BasePermission

class IsOrganizationAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # If obj is Membership → get organization
        if isinstance(obj, Membership):
            organization = obj.organization
        else:
            organization = obj  # Organization instance

        return Membership.objects.filter(
            user=request.user,
            organization=organization,
            role__in=["owner", "admin"]
        ).exists()
