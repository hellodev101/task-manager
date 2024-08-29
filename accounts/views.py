from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
# from .models import User
from django.db import IntegrityError

# Create your views here.

def register(request):
    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "accounts/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "accounts/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("tasks:index"))
    else:
        return render(request, "accounts/register.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        user = request.POST.get("username")  # Use .get() for safety
        password = request.POST.get("password") 
        user = authenticate(request, username=user, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "accounts/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "accounts/login.html")
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("tasks:index"))