from rest_framework import serializers

from cart.serializers import CartSerializer
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    order_items = CartSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'order_items', 'user', 'ordered', 'created']
