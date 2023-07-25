from datetime import timedelta

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.db.utils import IntegrityError
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
import phonenumbers

from users.models import VerificationCode, CustomUser
from users.serializers import UserRegistrationSerializer, UserLoginSerializer, SendPhoneVerificationCodeSerializer, \
    CheckPhoneVerificationCodeSerializer, UserPhoneLoginSerializer, UserPhoneRegistrationSerializer
from .tasks import send_verification_code


class UserRegistrationAPIView(GenericAPIView):
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
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)


class SendPhoneVerificationCodeView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SendPhoneVerificationCodeSerializer

    @swagger_auto_schema(request_body=SendPhoneVerificationCodeSerializer)
    def post(self, request, *args, **kwargs):
        serializer = SendPhoneVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get("phone")
        code = get_random_string(allowed_chars="0123456789", length=6)
        verification_code, _ = (
            VerificationCode.objects.update_or_create(
                phone=phone, defaults={"code": code, "is_verified": False}
            )
        )
        verification_code.expired_at = verification_code.last_sent_time + timedelta(seconds=60)
        verification_code.save(update_fields=["expired_at"])
        send_verification_code.delay(phone, code)
        return Response({"detail": f"Telefon raqamga sms kod yuborildi"})


class CheckPhoneVerificationCodeView(CreateAPIView):
    queryset = VerificationCode.objects.all()
    serializer_class = CheckPhoneVerificationCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get("phone")
        code = serializer.validated_data.get("code")
        verification_code = self.get_queryset().filter(phone=phone, is_verified=False).order_by(
            "-last_sent_time").first()
        if verification_code and verification_code.code != code and verification_code.is_expire:
            raise ValidationError("Verification code invalid.")
        verification_code.is_verified = True
        verification_code.save(update_fields=["is_verified"])
        return Response({"detail": "Verification code is verified."})


class UserPhoneLoginAPIView(GenericAPIView):

    @swagger_auto_schema(request_body=UserPhoneLoginSerializer)
    def post(self, request):
        serializer = UserPhoneLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.save(), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPhoneRegistrationAPIView(APIView):

    @swagger_auto_schema(request_body=UserPhoneRegistrationSerializer)
    def post(self, request):
        serializer = UserPhoneRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
