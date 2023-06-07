from django.contrib.auth import authenticate
from rest_framework import serializers

from users.models import CustomUser


class CustomUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email')


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'password')


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
