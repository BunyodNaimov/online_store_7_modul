from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.utils import phone_validator


class CustomUser(AbstractUser):
    class UserTypes(models.TextChoices):
        SALESMAN = 'salesman'
        BUYER = 'buyer'
        ADMIN = 'admin'

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        }, )
    email = models.EmailField(_("email address"), unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, validators=[phone_validator])
    job = models.CharField(max_length=129, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_picture/', null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=50, choices=UserTypes.choices, default=UserTypes.BUYER)



    def __str__(self):
        if self.username:
            return self.username
        if self.phone:
            return self.phone
        if self.email:
            return self.email

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.type = 'admin'
        super(CustomUser, self).save(*args, **kwargs)


class VerificationCode(models.Model):
    class VerificationTypes(models.TextChoices):
        REGISTER = "register"
        LOGIN = "login"

    code = models.CharField(max_length=6)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="verification_codes", null=True, blank=True
    )
    email = models.EmailField(unique=True, null=True)
    phone = models.CharField(max_length=15, unique=True, null=True, validators=[phone_validator])
    verification_type = models.CharField(max_length=50, choices=VerificationTypes.choices)
    last_sent_time = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    expired_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.email

    class Meta:
        unique_together = ["phone", "verification_type"]

    @property
    def is_expire(self):
        return self.expired_at < self.last_sent_time + timedelta(seconds=30)
