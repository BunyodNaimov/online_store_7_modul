from django.contrib import admin

from products.models import Product, ProductImage, SpecificationAttribute, SpecificationValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = "name", "pk", "price", "category", "active", "created_at", "slug"
    list_display_links = "name", "pk"
    ordering = "pk",
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = "image", "product", "pk"
    list_display_links = "image", "pk"
    ordering = "pk",


@admin.register(SpecificationAttribute)
class SpecificationAttributeAdmin(admin.ModelAdmin):
    list_display = ("name", "pk")
    list_display_links = "name", "pk"
    ordering = "pk",


@admin.register(SpecificationValue)
class SpecificationValueAdmin(admin.ModelAdmin):
    list_display = "product", "pk", "value", "attribute"
    list_display_links = "attribute", "pk"
    ordering = "pk",
