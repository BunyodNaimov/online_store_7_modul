from rest_framework import serializers

from categories.models import Category
from categories.serializers import CategorySerializer
from products.models import Product, SpecificationAttribute, SpecificationValue, ProductImage


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class ProductListSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "price", "image", "category"]


class ProductCreateSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "price", "category"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["category"] = ProductCategorySerializer(instance.category).data
        return data


class SpecificationAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationAttribute
        fields = ['id', 'name']


class SpecificationValueSerializer(serializers.ModelSerializer):
    attribute = SpecificationAttributeSerializer()

    class Meta:
        model = SpecificationValue
        fields = ['attribute', 'value']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    specifications = SpecificationValueSerializer(many=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'specifications', 'description', 'price', 'category', 'images']
