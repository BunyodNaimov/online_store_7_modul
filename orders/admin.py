from django.contrib import admin

from orders.models import Order


admin.site.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = 'id', 'order_items', 'user', 'ordered', 'created'
