from django.utils import timezone
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Membership,
    Organization,
    Project,
    Task
)
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {
            "is_active": {"read_only": True}
        }
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.is_active = True
        user.set_password(password)
        user.save()

        return user
    
class PassworedUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id","username","password")
        extra_kwargs = {
            "is_active": {"read_only": True},
            "email" : {"read_only" : True},
            "username" : {"read_only" : True},
            "password" : {"write_only":True}
        }
    
    def update(self, instance, validated_data):
        password = validated_data.pop("password")
        instance.set_password(password)
        instance.save()

        return instance
    
class OrganizationSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = ("id", "name", "description")
        read_only_fields = ("id",)

    def validate_name(self, value):
        if Organization.objects.filter(name=value).exists():
            raise serializers.ValidationError("Organization with this name already exists.")
        return value

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        organization = Organization.objects.create(
            owner = user,
            **validated_data
        )

        Membership.objects.create(
            user = request.user,
            organization = organization,
            role='owner', 
            joined_at=timezone.now()
        )

        return organization
    
class InviteMemberSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role = serializers.ChoiceField(choices=["admin", "member"], default="member", required=False)

    def validate_user_id(self,value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist.")
        return value
    
    def validate(self, attrs):
        org = self.context["organization"]

        if Membership.objects.filter(
            user_id=attrs["user_id"],
            organization = org
        ).exists():
            raise serializers.ValidationError(
                "User is already a member of this organization."
            )

        return attrs
    
class MembershipsSerializer(ModelSerializer):
    class Meta:
        model = Membership
        fields = ("role",)

class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = (
            "id",
            "title",
            "description",
            "organization",
        )
        read_only_fields = ("id", "created_by")

    def create(self, validated_data):
        request = self.context["request"]

        return Project.objects.create(
            created_by=request.user,
            **validated_data
        )
    
class TaskCreateSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def validate_project(self, project):
        user = self.context["request"].user

        if not Membership.objects.filter(
            user = user,
            organization = project.organization
        ).exists():
            raise serializers.ValidationError(
                "Project does not belong to your organization."
            )

        return project
    
    def validate_assignee(self, assignee):
        if not assignee:
            return assignee
        
        user = self.context["request"].user
        project = self.initial_data.get("project")

        if not project:
            return assignee
        
        if not Membership.objects.filter(
            user=assignee,
            organization_id=project
        ).exists():
            raise serializers.ValidationError(
                "Assignee must belong to the same organization."
            )

        return assignee
    
    def validate_parent(self, parent):
        if not parent:
            return parent

        project_id = self.initial_data.get("project")

        if parent.project_id != int(project_id):
            raise serializers.ValidationError(
                "Parent task must belong to the same project."
            )

        return parent
    
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "project",
            "assignee",
            "status",
            "priority",
            "parent",
            "due_date",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]