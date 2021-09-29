
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
    path("edit_post/<int:post_id>", views.edit_post_view, name="edit_post"),
    path("like_post/<int:post_id>", views.like_post_view, name='like_post'),
    path("unlike_post/<int:post_id>", views.unlike_post_view, name='unlike_post'),
    path("follow/<str:profile_name>", views.follow_profile_view, name='follow'),
    path("unfollow/<str:profile_name>", views.unfollow_profile_view, name='unfollow'),
    path("<str:profile_name>/", views.ProfileView.as_view(), name='profile'),
]
