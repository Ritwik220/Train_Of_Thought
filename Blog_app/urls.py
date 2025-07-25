from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="Blog_app"),
    path('<str:name>', views.greet, name="greet")
]
