
from django.urls import path

from . import views

urlpatterns = [

    path("", views.IndexView.as_view(), name="index"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("register", views.RegisterView.as_view(), name="register"),
    # path("register", views.register, name="register"),
    path("following", views.FollowingView.as_view(), name="following"),
    path("edit", views.EditView.as_view(), name="edit"),
    path("<str:profile_name>", views.ProfileView.as_view(), name="profile"),
]
