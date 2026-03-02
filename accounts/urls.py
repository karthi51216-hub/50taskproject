
from django.urls import path
from .views import register_view, MyLoginView, MyLogoutView

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", MyLoginView.as_view(), name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
]