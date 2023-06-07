from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from pagination import CustomPageNumberPagination
from products.models import Product
from products.permissions import IsUserOrReadOnly
from products.serializers import ProductCreateSerializer, ProductListSerializer


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterer_fields = ('category', 'products')
    search_fields = ("title", "category__name")
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer

        return ProductListSerializer

    def get_permissions(self):
        if self.request.method in ("POST",):
            self.permission_classes = (permissions.IsAuthenticated,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()


class ProductUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return ProductCreateSerializer

        return ProductListSerializer

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            self.permission_classes = (IsUserOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)
        return super().get_permissions()
