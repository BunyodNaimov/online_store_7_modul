from rest_framework import serializers
from .models import Cart


class CartSerializer(serializers.ModelSerializer):
    item = serializers.StringRelatedField()

    class Meta:
        model = Cart
        fields = ('user', 'item', 'quantity', 'created')
