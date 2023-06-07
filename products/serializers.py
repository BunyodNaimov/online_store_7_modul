from rest_framework import serializers

from products.models import Product


class ProductListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'brand', 'category', 'description', 'price', 'image')


class ProductCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'brand', 'category', 'description', 'price')
