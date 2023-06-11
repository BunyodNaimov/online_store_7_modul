from rest_framework import serializers

from categories.models import Category


class CategoryParentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')

    def get_parent(self, obj):
        if obj.parent:
            return CategoryParentSerializers(obj.parent).data
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['parent'] = CategoryParentSerializers(instance.parent).data
        return data
