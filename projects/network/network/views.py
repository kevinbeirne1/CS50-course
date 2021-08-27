from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import CreateView

from .models import User


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            login_success_message = "Log In Completed"
            messages.add_message(request, messages.SUCCESS,
                                 login_success_message)
            return redirect("network:index")
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


class RegisterView(CreateView):
    template_name = "network/register.html"
    model = User


def register(request):
    if request.method == "POST":
        try:
            username = request.POST["username"]
            email = request.POST["email"]

            # Ensure password matches confirmation
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
            if password != confirmation:
                password_confirmation_error = "Passwords Do Not Match"
                messages.add_message(request, messages.ERROR,
                                     password_confirmation_error)
                return render(request, "network/register.html")

            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                duplicate_account_error = "Username Already Taken"
                messages.add_message(request, messages.ERROR,
                                     duplicate_account_error)
                return render(request, "network/register.html")

            login(request, user)
            register_success_message = "New Account Created"
            messages.add_message(request, messages.SUCCESS,
                                 register_success_message)
            return redirect('network:index')
            # return HttpResponseRedirect(reverse("network:index"))
        except MultiValueDictKeyError:
            messages.error(request, "All Boxes Are Required")
            return redirect('network:register')
            # return  render(request, "network/register.html")

    else:
        return render(request, "network/register.html")
