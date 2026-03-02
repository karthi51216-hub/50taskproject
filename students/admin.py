from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone", "dept", "created_at")
    search_fields = ("name", "email", "phone", "dept")
    list_filter = ("dept", "created_at")
    ordering = ("-created_at",)
    