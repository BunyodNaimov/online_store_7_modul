from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from categories.models import Category
from categories.serializers import CategorySerializer
from pagination import CustomPageNumberPagination


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.order_by('name')
    serializer_class = CategorySerializer

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('category', 'brand')
    search_fields = ('name', 'description')
    ordering_fields = ('price', 'created_at')
    pagination_class = CustomPageNumberPagination

    def get_permissions(self):
        if self.request.method in ("POST",):
            self.permission_classes = (permissions.IsAuthenticated,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()

    @swagger_auto_schema(request_body=CategorySerializer)
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        category = Category.objects.filter(pk=pk).first()
        if category is None:
            Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CategorySerializer)
    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
