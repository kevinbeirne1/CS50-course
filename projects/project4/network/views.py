from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView as LoginViewBase
from django.contrib.auth.views import LogoutView as LogoutViewBase
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView

from .models import Post, User
from .forms import CreateUserForm

def index(request):
    return render(request, "network/index.html")


class IndexView(ListView):
    template_name = "network/index.html"
    model = Post
    paginate_by = 10


class LoginView(SuccessMessageMixin, LoginViewBase):
    template_name = "network/login.html"
    success_message = "Login Successful"
    login_failed_message = "Invalid username and/or password."
    success_url = reverse_lazy("index")
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, self.login_failed_message)
        return super().form_invalid(self)

    def get_success_url(self):
        return str(self.success_url)


# def login_view(request):
#     if request.method == "POST":
#
#         # Attempt to sign user in
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = authenticate(request, username=username, password=password)
#
#         # Check if authentication successful
#         if user is not None:
#             login(request, user)
#             return HttpResponseRedirect(reverse("index"))
#         else:
#             return render(request, "network/login.html", {
#                 "message": "Invalid username and/or password."
#             })
#     else:
#         return render(request, "network/login.html")


class LogoutView(SuccessMessageMixin, LogoutViewBase):
    success_message = "Logged out Successfully"
    next_page = "/"


class RegisterView(CreateView):
    template_name = "network/register.html"
    model = User
    form_class = CreateUserForm
    success_url = reverse_lazy('index')
    permission_denied_message = "You're already logged in"

    def form_valid(self, form):
        """Save user form, login user and redirect to success_url"""
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        return str(self.success_url)

    def get(self, request, *args, **kwargs):
        """Return to index if user is logged in"""
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().get(self, request, args, kwargs)


"""
# Original register FBV
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["repeat_password"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
"""

class ProfileView(TemplateView):
    template_name = "network/profile.html"
    pass


def profile(request, profile_name):
    # return HttpResponse(profile_name)
    print("test", profile_name)
    return render(request, "network/profile.html", {
        "profile_name": profile_name,
    })


class FollowingView(TemplateView):
    template_name = "network/following.html"
    pass


def following(request):
    return render(request, "network/following.html", {
        # "profile_name": profile_name,
    })


class EditView(TemplateView):
    template_name = "network/edit.html"
    pass


def edit(request):
    return render(request, "network/edit.html", {
        # "profile_name": profile_name,
    })
