from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _

import users.models
from users.models import CustomUser, VerificationCode
from users.utils import phone_validator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id", "username", "email", "first_name", "last_name", "phone", "birth_date", "age", "type"
        )


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Класс Serializer для аутентификации пользователей с помощью имени пользователя и пароля.
    """
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('username', 'password')

    def validate(self, attrs):
        try:
            user = CustomUser.objects.get(username=attrs['username'])
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('Неправильные учетные данные')

        user = authenticate(username=user.username, password=attrs['password'])

        if user and user.is_active:
            return user

        raise serializers.ValidationError("Неправильные учетные данные")


class SendPhoneVerificationCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, validators=[phone_validator])

    class Meta:
        model = VerificationCode
        fields = ("phone",)


class CheckPhoneVerificationCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, validators=[phone_validator])
    code = serializers.CharField(min_length=6, max_length=6)
    username = serializers.CharField(max_length=15, allow_blank=True)
