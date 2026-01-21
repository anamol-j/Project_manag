from rest_framework.viewsets import ModelViewSet
from .serializers import (
    UserSerializer,
    PassworedUpdateSerializer
)
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
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