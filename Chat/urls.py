from django.urls import path
from . import views

urlpatterns = [
    path("", views.chat),
    path("home", views.chat_home),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
]
