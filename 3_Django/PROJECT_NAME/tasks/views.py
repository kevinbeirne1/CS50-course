from . import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse

# tasks = ["foo", "bar", "baz", ]


def index(request):
    # need to run python manage.py migrate before can use below variable

    if 'tasks' not in request.session:
        request.session['tasks'] = []
    return render(request, "tasks/index.html", {
        "tasks": request.session['tasks'],
    })


def add(request):
    # Check if method is POST
    if request.method == "POST":
        # Take in the data the user submitted and save it as a variable
        form = forms.NewTaskForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the task from the 'cleaned' version of form data
            task = form.cleaned_data["task"]
            # Add the new task to our list of tasks
            # tasks.append(task)

            request.session['tasks'] += [task]

            # Redirect user to list of tasks
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "tasks/add.html", {
                "form": form
            })

    return render(request, "tasks/add.html", {
        "form": forms.NewTaskForm()
    })

#
# class NewTaskForm(forms.Form):
#     task = forms.CharField(label="New Task")