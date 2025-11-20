from django.contrib.auth.models import User
from rest_framework import generics, mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import RegistrationSerializer, LoginSerializer

# View for user registration with token generation
class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # Generate or retrieve authentication token for the new user
        token, created = Token.objects.get_or_create(user=user)

        response_data = {
            "token": token.key, 
            "fullname": user.profile.full_name,
            "email": user.email,
            "user_id": user.id
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

# View for user login with token generation
class LoginView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.get()

        # Generate or retrieve authentication token for authenticated user
        token, created = Token.objects.get_or_create(user=user)

        response_data = {
            "token": token.key, 
            "fullname": user.profile.full_name,
            "email": user.email,
            "user_id": user.id
        }

        return Response(response_data, status=status.HTTP_200_OK)