from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import CustomUser, Chats
from django.db.utils import OperationalError


# Create your views here.
# Home Page
def chat_home(request):
    if request.user.is_authenticated:
        print("User is authenticated")
        return redirect('/Chat/')
    return render(request=request, template_name="Chat_Home.html")


def chat(request):
    user = request.user
    if user.username:
        print("Username: ", user.username)
        return render(request=request, template_name='chat.html', context={"userop": user, "users": CustomUser.objects.all()})
    else:
        return HttpResponseRedirect("register")


def register(request):
    if request.method == "GET":
        return render(request=request, template_name="Register.html")
    elif request.method == "POST":
        print("Submit button pressed")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = CustomUser.objects.create_user(email=email, password=password, username=username)
            user.save()
            print("User saved")
            user = authenticate(username=user.username, password=user.password)
            request.user = user
            login(request, user)
            print("User saved")
            return HttpResponseRedirect("Chat")
        except Exception as e:
            print(f"Error: {e}")
            raise Exception("Could not create user")


def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        print("Submit button pressed")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)
        request.user = user
        if user is not None:
            print("User authenticated")
            login(request, user)
            return redirect('/Chat/')
        else:
            print("Invalid credentials ", user)
            return render(request=request, template_name="login.html", context={"error": "Invalid credentials"})
