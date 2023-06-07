from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):

    class UserTypes(models.TextChoices):
        SALESMAN = 'salesman'
        BUYER = 'buyer'
        ADMIN = 'admin'

    email = models.EmailField(_("email address"), unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    job = models.CharField(max_length=129, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_picture/', null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=50, choices=UserTypes.choices, default=UserTypes.BUYER)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.type = 'admin'
        super(CustomUser, self).save(*args, **kwargs)
