from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Membership

class OrganizationRolePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        membership = Membership.objects.filter(
            user = user,
            organization = obj
        ).first()
        
        if not membership:
            return False
        
        role = membership.role
        
        if request.method in SAFE_METHODS:
            return role in [
                Membership.ROLE_OWNER,
                Membership.ROLE_ADMIN,
                Membership.ROLE_MEMBER
            ]
            
        if request.method == "POST":
            return role in [
                Membership.ROLE_OWNER,
                Membership.ROLE_ADMIN
            ]
            
        if request.method in ["PUT","PATCH","DELETE"]:
            return role in [
                Membership.ROLE_OWNER,
                Membership.ROLE_ADMIN
            ]
        return False