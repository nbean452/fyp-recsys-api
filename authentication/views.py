from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer

# Create your views here.


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        user = User.objects.get(username=request.data["username"])

        json_response = {
            "username": user.username,
            "email": user.email,
            "id": user.pk,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "token": {
                **serializer.validated_data
            }
        }

        return Response(json_response, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView, TokenObtainPairSerializer):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        user = User.objects.get(username=serializer.data["username"])
        refresh = self.get_token(user)

        json_response = {
            "username": user.username,
            "email": user.email,
            "id": user.pk,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "token": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }

        return Response(json_response, status=status.HTTP_201_CREATED, headers=headers)
