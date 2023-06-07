from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserRegistrationSerializer, UserLoginSerializer, CustomUserSerializers


# Create your views here.

class UserRegistrationAPIView(GenericAPIView):
    # Конечная точка для создания нового пользователя.

    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['tokens'] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_201_CREATED)


class UserLoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = serializers.validated_data
        serializers = CustomUserSerializers(user)
        token = RefreshToken.for_user(user)
        data = serializers.data
        data['token'] = {'refresh': str(token), 'access': str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)


