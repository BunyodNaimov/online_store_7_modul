from rest_framework import status, permissions
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order
from products.models import Product
from .models import Cart
from .serializers import CartSerializer


class CartListAPIView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class AddToCartView(APIView):

    """AddToCartView sinfi APIView asosida yaratilgan. POST so'roviga pk qiymati yuboriladi.
    Product modelidan pk maydoni orqali mahsulot olinadi. Olinadigan pk qiymati har bir
    mahsulot uchun unikal id hisoblanadi. Cart obyekti olinadi yoki yaratiladi. Order obyekti
    olinadi va Order obyektida mahsulotni topish uchun filter yordamidan foydalaniladi.
    Order obyektida mahsulot mavjud bo'lsa, Cart obyektiga qo'shiladi. Aks holda, yangi
    Order obyekti yaratiladi va Cart obyektiga qo'shiladi. serializer yordamida JSON formatida
    qaytariladi. Agar pk qiymati Product modelida mavjud emas bo'lsa, NotFound istisnasi qaytariladi."""

    def post(self, request, product_id):
        try:
            item = Product.objects.get(pk=product_id)
            order_item, created = Cart.objects.get_or_create(
                item=item,
                user=request.user
            )
            order_qs = Order.objects.filter(user=request.user, ordered=False)
            if order_qs.exists():
                order = order_qs[0]
                # check if the orders item is in the orders
                if order.order_items.filter(item__pk=product_id).exists():
                    order_item.quantity += 1
                    order_item.save()
                    serializer = CartSerializer(order_item)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    order.order_items.add(order_item)
                    serializer = CartSerializer(order_item)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                order = Order.objects.create(
                    user=request.user
                )
                order.order_items.add(order_item)
                serializer = CartSerializer(order_item)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            raise NotFound('Product not found')


class RemoveFromCartView(APIView):

    """RemoveFromCartView sinfi APIView asosida yaratilgan.
    POST so'roviga pk qiymati yuboriladi. Product modelidan pk maydoni orqali mahsulot olinadi.
    Olinadigan pk qiymati har bir mahsulot uchun unikal id hisoblanadi.
    Cart obyekti olib tashlanadi va quantity maydoni tekshiriladi. Agar quantity 1 dan katta bo'lsa,
    soni 1 kamaytiriladi. Aks holda, Cart obyekti o'chiriladi. Order obyekti olinadi va
    Order obyektida mahsulotni topish uchun filter yordamidan foydalaniladi. Order obyektida
    mahsulot mavjud bo'lsa, Cart obyektidan olib tashlanadi va serializer yordamida JSON formatida
    qaytariladi. Agar pk qiymati Product modelida mavjud emas yoki Cart obyekti topilmay qoldirilgan
    bo'lsa, NotFound istisnasi qaytariladi."""

    def post(self, request, product_id):
        try:
            item = Product.objects.get(pk=product_id)
            cart_qs = Cart.objects.filter(user=request.user, item=item)
            if cart_qs.exists():
                cart = cart_qs[0]
                # Checking the cart quantity
                if cart.quantity > 1:
                    cart.quantity -= 1
                    cart.save()
                else:
                    cart_qs.delete()
            order_qs = Order.objects.filter(
                user=request.user,
                ordered=False
            )
            if order_qs.exists():
                order = order_qs[0]
                # check if the orders item is in the orders
                if order.order_items.filter(item__pk=product_id).exists():
                    order_item = Cart.objects.filter(
                        item=item,
                        user=request.user,
                    )[0]
                    order.order_items.remove(order_item)
                    serializer = CartSerializer(cart)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            raise NotFound('Cart item not found')
        except Product.DoesNotExist:
            raise NotFound('Product not found')
        except IndexError:
            raise NotFound('Cart item not found')
