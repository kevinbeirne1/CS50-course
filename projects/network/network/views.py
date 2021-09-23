import json
from json import JSONDecodeError

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView as LoginViewBase
from django.contrib.auth.views import LogoutView as LogoutViewBase
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import CreateUserForm, EditPostForm, NewPostForm
from .models import Post, User

REGISTER_SUCCESS_MESSAGE = "New Account Created"
LOGIN_SUCCESS_MESSAGE = "Log In Completed"
LOGIN_FAILURE_MESSAGE = "Invalid username and/or password"
LOGOUT_SUCCESS_MESSAGE = "Logged out successfully"
LOGIN_REQUIRED_MESSAGE = "Login Required"


class IndexView(ListView):
    template_name = "network/index.html"
    model = Post
    paginate_by = 10


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


class ProfileView(ListView):
    model = Post
    template_name = "network/profile.html"
    paginate_by = 10

    def get_queryset(self):
        self.profile = get_object_or_404(
            User, username=self.kwargs['profile_name'])
        return Post.objects.filter(creator=self.profile)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['profile'] = self.profile
        return context


class FollowingView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "network/following.html"
    paginate_by = 10

    def handle_no_permission(self):
        """
        Add error message & redirect if anonymous user accesses view
        """
        messages.add_message(self.request, messages.ERROR,
                             LOGIN_REQUIRED_MESSAGE)
        return redirect('network:login')

    def get_queryset(self):
        """
        Get QuerySet of all posts by accounts user follows
        """
        following = self.request.user.following.all()
        return Post.objects.filter(creator__in=following)


def edit_post_view(request):
    if request.method == 'PUT':
        request_data = request.body
        form = EditPostForm(data=request_data, user=request.user)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204)

    return redirect('network:index')
