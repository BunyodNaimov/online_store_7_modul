from rest_framework import serializers

from categories.models import Category


class CategoryParentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CategorySerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name')


class CategoryCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['parent'] = CategoryParentSerializers(instance.parent).data
        return data
