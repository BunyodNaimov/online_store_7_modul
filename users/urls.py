from django.urls import path

from users.views import UserRegistrationAPIView, UserLoginAPIView, SendPhoneVerificationCodeView, \
    CheckPhoneVerificationCodeView, UserPhoneLoginAPIView, UserPhoneRegistrationAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path("phone/send-verification-code/", SendPhoneVerificationCodeView.as_view(), name='send_phone_code'),
    path("phone/check-verification-code/", CheckPhoneVerificationCodeView.as_view(), name="check-phone-code"),
    path("phone/phone-login/", UserPhoneLoginAPIView.as_view(), name='user-phone-login'),
    path('phone/phone-register/', UserPhoneRegistrationAPIView.as_view(), name='user-phone-register'),

]

