from django.urls import path
from . import views

urlpatterns = [
    path('', views.new_year, name="New Year"),
]
