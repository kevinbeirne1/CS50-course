from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import CreateView

from .forms import CreateUserForm
from .models import User

REGISTER_SUCCESS_MESSAGE = "New Account Created"
LOGIN_SUCCESS_MESSAGE = "Log In Completed"


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
            messages.add_message(request, messages.SUCCESS,
                                 LOGIN_SUCCESS_MESSAGE)
            return redirect("network:index")
        else:
            messages.add_message(request, messages.WARNING,
                                 "Invalid username and/or password.")
            return render(request, "network/login.html")
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


class RegisterView(CreateView):
    template_name = "network/register.html"
    model = User
    form_class = CreateUserForm
    success_url = reverse_lazy('network:index')
    permission_denied_message = "You're already logged in"

    def form_valid(self, form):
        """Save user form, login user and redirect to success_url"""
        user = form.save()
        login(self.request, user)
        register_success_message = "New Account Created"
        messages.add_message(self.request, messages.SUCCESS,
                             REGISTER_SUCCESS_MESSAGE)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        return str(self.success_url)

    def get(self, request, *args, **kwargs):
        """Return to index if user is logged in"""
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().get(self, request, args, kwargs)



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
