from django import forms
from django.shortcuts import render
from django.http import HttpResponse


class Form(forms.Form):
    new_task = forms.CharField(label="New Task")


def index(request):
    if "tasks" not in request.session:
        request.session['tasks'] = []
    return render(request, "index.html", {
        "tasks": request.session["tasks"]
    })


def add(request):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            task = form.cleaned_data['new_task']
            request.session["tasks"] += [task] 
        else:
            return render(request, "add.html", {
                "form": form,
            })
    return render(request, "add.html", {
        "form": Form()
    })
