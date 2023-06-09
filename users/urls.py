from django.urls import path

from users.views import UserRegistrationAPIView, UserLoginAPIView, SendPhoneVerificationCodeView, \
    CheckPhoneVerificationCodeView, PhoneLoginView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path("phone/verification-code/", SendPhoneVerificationCodeView.as_view(), name='send_phone_code'),
    path("phone/check-verification-code/", CheckPhoneVerificationCodeView.as_view(), name="check-email"),
    path("phone/get_token/", PhoneLoginView.as_view(), name="phone_get_token"),

]
