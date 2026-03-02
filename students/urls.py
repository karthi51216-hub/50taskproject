
from django.urls import path
from . import views

urlpatterns = [
    path("", views.student_list, name="student_list"),
    path("new/", views.student_create, name="student_create"),
    path("<int:pk>/edit/", views.student_edit, name="student_edit"),
    path("<int:pk>/delete/", views.student_delete, name="student_delete"),
    path("bulk-delete/", views.student_bulk_delete, name="student_bulk_delete"),
]