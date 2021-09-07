from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as LoginViewBase
from django.contrib.auth.views import LogoutView as LogoutViewBase
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import CreateView, DetailView, ListView

from .forms import CreateUserForm, NewPostForm
from .models import Post, User

REGISTER_SUCCESS_MESSAGE = "New Account Created"
LOGIN_SUCCESS_MESSAGE = "Log In Completed"
LOGIN_FAILURE_MESSAGE = "Invalid username and/or password"
LOGOUT_SUCCESS_MESSAGE = "Logged out successfully"


def index(request):
    return render(request, "network/index.html")


class IndexView(ListView):
    template_name = "network/index.html"
    model = Post


class LoginView(SuccessMessageMixin,  LoginViewBase):
    template_name = "network/login.html"
    success_message = LOGIN_SUCCESS_MESSAGE
    success_url = "/"

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR,
                             LOGIN_FAILURE_MESSAGE)
        return super(LoginView, self).form_invalid(form)


class LogoutView(LogoutViewBase):
    next_page = '/'

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.SUCCESS, LOGOUT_SUCCESS_MESSAGE)
        return super(LogoutView, self).dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    template_name = "network/register.html"
    model = User
    form_class = CreateUserForm
    success_url = reverse_lazy('network:index')

    def form_valid(self, form):
        """Save user form, login user and redirect to success_url"""
        url = super(RegisterView, self).form_valid(form)
        user = form.save()
        login(self.request, user)
        messages.add_message(self.request, messages.SUCCESS,
                             REGISTER_SUCCESS_MESSAGE)
        return url

    def get(self, request, *args, **kwargs):
        """Return to index if user is logged in"""
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(self, request, args, kwargs)


class NewPostView(LoginRequiredMixin, CreateView):
    template_name = "network/new_post.html"
    model = Post
    form_class = NewPostForm
    success_url = reverse_lazy('network:index')

    def handle_no_permission(self):
        return redirect('network:index')
