from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse


def new_year(request):
    now = datetime.now()
    return render(request, "new_year/new_year.html",{
        "new_year": now.month == 1 and now.day == 1,
                   })
    # return HttpResponse('hello')
