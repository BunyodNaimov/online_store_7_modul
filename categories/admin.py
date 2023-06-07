from django.contrib import admin

from categories.models import Category
from products.models import Brand


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "name", "pk"
    list_display_links = "name", "pk"
    ordering = "pk",
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = "name", "pk"
    list_display_links = "name", "pk"
    ordering = "pk",
    prepopulated_fields = {'slug': ('name',)}
