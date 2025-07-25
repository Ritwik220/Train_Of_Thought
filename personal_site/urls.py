from django.urls import path
from . import views

urlpatterns = [
    path("", views.first_page, name="first_page"),
    path("Home", views.introduction, name="introduction"),
    path("Home/", views.introduction, name="introduction"),
    path("Projects", views.projects, name="projects"),
    path("Projects/", views.projects, name="projects")
]
