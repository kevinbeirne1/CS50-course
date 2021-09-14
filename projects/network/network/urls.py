
from django.urls import path

from . import views

app_name = 'network'

urlpatterns = [
    path("", views.IndexView.as_view(), name='index'),
    path("login/", views.LoginView.as_view(), name='login'),
    path("logout", views.LogoutView.as_view(), name='logout'),
    path("register/", views.RegisterView.as_view(), name='register'),
    path("new_post/", views.NewPostView.as_view(), name='new_post'),
    path("following/", views.FollowingView.as_view(), name='following'),
    path("<str:profile_name>/", views.ProfileView.as_view(), name='profile'),
]
