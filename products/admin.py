from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "category", "created_at")
    search_fields = ("title", "category")
    list_filter = ("category",)
    ordering = ("-created_at",)