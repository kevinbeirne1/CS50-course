from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "APP_NAME/index.html")


def brian(request):
    return HttpResponse("Hello Brian!")


def david(request):
    return HttpResponse("Hello David!")


def greet(request, name):
    return render(request, "APP_NAME/greet.html",
                  {"name": name.capitalize()})
    # return HttpResponse(f"Hello, {name}!")