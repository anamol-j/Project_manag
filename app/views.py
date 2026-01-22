from rest_framework.viewsets import ModelViewSet
from .permission import IsOrganizationAdmin
from rest_framework.decorators import action
from .serializers import (
    UserSerializer,
    PassworedUpdateSerializer,
    OrganizationSerializer,
    InviteMemberSerializer,
    MembershipsSerializer,
    ProjectSerializer
)
from .models import (
    Membership,
    Organization,
    Project,
    Task
)
from django.http import Http404
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

class UserViewsetAPI(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all() 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if len(request.data['password']) < 8:
            return Response({
                "message" : "Password must be 8 char long",
                "status": status.HTTP_200_OK
            })
        
        self.perform_create(serializer)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    
class PassworedUpdateAPI(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PassworedUpdateSerializer
    queryset = User.objects.all() 
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
            )
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response({
            "message" : "Updated",
            "data" : serializer.data,
            "status" : status.HTTP_200_OK
        })
    
class OrganizationViewSetAPI(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Organization.objects.all()

        return Organization.objects.filter(owner = user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": "Organization list",
            "status": status.HTTP_200_OK,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            "message": "Organization details",
            "status": status.HTTP_200_OK,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            "massage": "Organization Created.",
            "data": serializer.data,
            "status":status.HTTP_201_CREATED
        })
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if request.data['name'] == instance.name:
            return Response({
                "massage" : "Organization name should different from previews one",
                "status": status.HTTP_400_BAD_REQUEST
            })
        serializer = self.get_serializer(instance, data=request.data,partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            "massage" : "Updated",
            "status": status.HTTP_200_OK
        })

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return Response({
                "message": "Organization not found",
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(instance)

        return Response({
            "message": "Deleted successfully",
            "status": 200
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["post"], permission_classes=[IsOrganizationAdmin])
    def invite(self, request, pk=None):
        organization = self.get_object()
        print(organization)
        serializer = InviteMemberSerializer(
            data=request.data,
            context={"organization": organization}
        )
        serializer.is_valid(raise_exception=True)
        
        Membership.objects.create(
            user_id = serializer.validated_data['user_id'],
            organization = organization,
            role = serializer.validated_data['role']
        )

        return Response({
            "message": "User invited successfully",
            "status": status.HTTP_201_CREATED
        }, status=status.HTTP_201_CREATED)
    
class MembershipsViewSetAPI(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = MembershipsSerializer
    queryset = Membership.objects.all()

    def destroy(self, request, *args, **kwargs):
        membership = self.get_object()
        self.perform_destroy(membership)

        return Response({
            "message": "Member removed successfully",
            "status": status.HTTP_200_OK
        })
class ProjectViewSetAPI(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            "message": "Project added successfully",
            "data" : serializer.data
        },status.HTTP_201_CREATED)