from django.urls import path

from products.views import ProductListCreateAPIView, ProductUpdateDeleteAPIView

app_name = 'products'
urlpatterns = [
    path('', ProductListCreateAPIView.as_view(), name='product_list_create'),
    path('<int:pk>/', ProductUpdateDeleteAPIView.as_view(), name='product_update_delete'),
]
