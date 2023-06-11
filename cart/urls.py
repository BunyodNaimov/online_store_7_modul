from django.urls import path

from .views import AddToCartView, RemoveFromCartView, CartListAPIView

app_name = 'cart'

urlpatterns = [
    path('', CartListAPIView.as_view(), name='cart-list'),
    path('add-to-cart/<int:product_id>', AddToCartView.as_view(), name='add-to-cart'),
    path('remove-from-cart/<int:product_id>', RemoveFromCartView.as_view(), name='remove-from-cart'),
]
