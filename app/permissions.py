from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import (
    Membership,
    Project
)

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
    
class ProjectRolePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        
        if not request.user.is_authenticated:
            return False
        
        if request.method == "POST":
            org_id = request.data.get("organization")
            print(org_id)

            membership = Membership.objects.filter(
                user = user,
                organization_id = org_id
            ).first()

            if not membership:
                return False
            
            return membership.role in [
                Membership.ROLE_OWNER,
                Membership.ROLE_ADMIN
            ]
        return True
    
    def has_object_permission(self, request, view, obj):
        user = request.user

        membership = Membership.objects.filter(
            user = user,
            organization_id = obj.organization
        ).first()

        if not membership:
            return False
        
        if request.method in SAFE_METHODS:
            return True

        return membership.role in [
                Membership.ROLE_OWNER,
                Membership.ROLE_ADMIN
            ]