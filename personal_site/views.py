from django.shortcuts import render, redirect
# import json

projects_made = [{
    "name": "Train of Thought",
    "description": "A website where you can write blogs which can be made public or kept private, you can also read the"
                   " blogs other people have made public.",
    "url": "train-of-thought",
    "img": "Favicon/android-chrome-192x192.png"},
    {
        "name": "ChatVerse",
        "description": "A website where you can chat with your friends, colleagues, etc.",
        "url": "Chat/home",
        "img": "Chat_Logo.png"
    }
]


# Create your views here.
def introduction(request):
    return render(request=request, template_name="personal_website.html")


# Redirecting the user to the home page in case no additional information is given.
def first_page(request):
    print(request)
    return redirect("/Home")


# Rendering the projects html file.
def projects(request):
    return render(request, "projects.html", {"projects": projects_made})
