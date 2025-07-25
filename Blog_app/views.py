from django.shortcuts import render, redirect
from django.http import HttpResponse


# Create your views here.
def home_page(request):
    return render(request, "train_of_thought.html")


def greet(request, name):
    return render(request, "greet.html", {
        "name": name.capitalize()
    })
