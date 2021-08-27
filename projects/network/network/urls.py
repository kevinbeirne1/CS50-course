
from django.urls import path

from . import views

app_name = 'network'

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    # path("register", views.RegisterView.as_view(), name='register'),
    path("register", views.register, name="register"),
]
