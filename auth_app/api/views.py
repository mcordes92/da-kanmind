from django.contrib.auth.models import User
from rest_framework import generics, mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import RegistrationSerializer, LoginSerializer


class RegistrationView(generics.CreateAPIView):
    """View for user registration with token generation."""

    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        """Create a new user and generate authentication token."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)

        response_data = {
            "token": token.key, 
            "fullname": user.profile.full_name,
            "email": user.email,
            "user_id": user.id
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginView(mixins.ListModelMixin, generics.GenericAPIView):
    """View for user login with token generation."""

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        """Authenticate user and generate authentication token."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.get()

        token, created = Token.objects.get_or_create(user=user)

        response_data = {
            "token": token.key, 
            "fullname": user.profile.full_name,
            "email": user.email,
            "user_id": user.id
        }

        return Response(response_data, status=status.HTTP_200_OK)