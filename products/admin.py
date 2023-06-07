from django.contrib import admin
from django.utils.text import slugify

from products.models import Product, ProductSpecification, ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = "title", "pk", "price", "category", "active", "created_at", "slug"
    list_display_links = "title", "pk"
    ordering = "pk",
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = "name", "pk", "product"
    list_display_links = "name", "pk"
    ordering = "pk",


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = "name", "pk", "value", "product"
    list_display_links = "name", "pk"
    ordering = "pk",
