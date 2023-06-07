from django.shortcuts import render
from rest_framework import generics

from categories.models import Category
from categories.serializers import CategorySerializers, CategoryCreateSerializers


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryCreateSerializers
        return CategorySerializers

