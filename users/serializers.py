from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers, exceptions

import phonenumbers
from rest_framework.authtoken.models import Token

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


class UserPhoneLoginSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ("phone",)

    def validate_phone_number(self, phone):
        parsed_number = phonenumbers.parse(phone, "US")
        if not phonenumbers.is_valid_number(parsed_number):
            raise serializers.ValidationError("Invalid phone number")
        return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)

    def validate(self, data):
        phone = data.get("phone")

        user = CustomUser.objects.get(phone=phone)

        if user is None:
            raise serializers.ValidationError("Invalid phone number or password")

        data["user"] = user
        return data

    def create(self, validated_data):
        user = validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return {"token": token.key}


class UserPhoneRegistrationSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=15)

    class Meta:
        model = CustomUser
        fields = ("id", "phone", "password")
        extra_kwargs = {"password": {"write_only": True}, "id": {"read_only": True}}

    def validate_phone_number(self, phone_number):
        parsed_number = phonenumbers.parse(phone_number, "US")
        if not phonenumbers.is_valid_number(parsed_number):
            raise serializers.ValidationError("Invalid phone number")
        return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)

    def create(self, validated_data):
        phone_number = validated_data.pop("phone")
        validated_data["phone"] = phone_number
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
