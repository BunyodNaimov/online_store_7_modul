from django.db import models

from cart.models import Cart
from users.models import CustomUser


# Order Model
class Order(models.Model):
    order_items = models.ManyToManyField(Cart)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
