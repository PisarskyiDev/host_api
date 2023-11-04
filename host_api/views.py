from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework import views
from rest_framework.response import Response

from cmd_command import ssh_shutdown_host
from .models import User
from .serializers import UserSerializer, UserCreateSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = (IsAdminUser,)


class UsersListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class UsersDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class SelfUserProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    queryset = User.objects

    def get_object(self):
        return self.request.user


class ShutdownView(views.APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        ssh_shutdown_host()
        return Response({"result": "OK"}, status=status.HTTP_200_OK)
