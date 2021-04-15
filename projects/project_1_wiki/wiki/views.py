from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
import random
import copy

from . import forms
import markdown2


app_name = "wiki"

# pages = {"Hello": "world", "Monty": "pyt<i>hon</i>", "Hel1lo1": "world",
#          "Hello2": "world", "Hel3ello3": "world"}

# in time replace pages with request.session


def index(request):
    # names = list(request.session['pages'])
    # return HttpResponse(names[-1])
    if 'pages' not in request.session:
        request.session['pages'] = {}

    return render(request, f"{app_name}/index.html", {
        "pages": request.session['pages'],
        "title": 'Homepage',
        "search_form": forms.SearchForm(),
    })


def entry(request, entry_name):
    if entry_name != entry_name.capitalize():
        return HttpResponseRedirect(f"/{app_name}/{entry_name.capitalize()}")

    if entry_name not in request.session['pages']:
        return error_page(request)

    entry_markdown = request.session['pages'][entry_name]
    return render(request, f"{app_name}/entry.html", {
        "entry_name": entry_name,
        "entry_markdown": markdown2.markdown(entry_markdown),
        "search_form": forms.SearchForm(),
    })


def search(request):
    form = forms.SearchForm(request.GET)
    partial_matches = []
    if form.is_valid():
        search_name = form.clean_search_name()
        for page in request.session['pages']:
            if search_name == page:
                return HttpResponseRedirect(f"/{app_name}/{search_name}")
            elif search_name in page:
                partial_matches.append(page)
        return render(request, f"{app_name}/search.html", {
            "search_name": forms.SearchForm(initial={"search_name": search_name}),
            "partial_matches": partial_matches,
            "search_form": forms.SearchForm(),
        })
    return render(request, f"{app_name}/search.html", {
            "search_name": forms.SearchForm(),
            "search_form": forms.SearchForm(),
        })


def new_page(request):
    if request.method == "POST":
        form = forms.NewEntryForms(request.POST)
        if form.is_valid():
            entry_name = form.cleaned_data['entry_name']
            entry_markdown = form.cleaned_data['entry_markdown']
            if entry_name in request.session['pages']:
                return error_page(request)
            else:
                request.session['pages'].update({entry_name: entry_markdown})
                request.session.save()
            return HttpResponseRedirect(f"/{app_name}/{entry_name}")

    return render(request, "wiki/new_page.html", {
        "form": forms.NewEntryForms(),
        "search_form": forms.SearchForm(),
    })


def edit_page(request):
    if request.method == "POST":
        form = forms.NewEntryForms(request.POST)

        if form.is_valid():
            entry_name = form.cleaned_data["entry_name"]

            entry_markdown = form.cleaned_data["entry_markdown"]
            # update_request_session(request.session, {entry_name: entry_markdown})
            request.session['pages'].update({entry_name: entry_markdown })
            request.session.save
            return HttpResponseRedirect(f"/{app_name}/{entry_name}")

        else:
            entry_name = form.cleaned_data["entry_name"]
            # return HttpResponse(entry_name)
            entry_markdown = request.session['pages'][entry_name]
            return render(request, f"{app_name}/edit_page.html", {
                "entry_name": entry_name,
                "entry_markdown": entry_markdown,
                "search_form": forms.SearchForm(),
            })


def error_page(request):
    return render(request, f"{app_name}/error_page.html", {
        "title": "Error Page",
        "search_form": forms.SearchForm(),
    })


def random_page(request):
    chosen_page = random.choice(list(request.session['pages']))
    return redirect(f"/{app_name}/{chosen_page}")


def update_request_session(request_session, entry_details):
    copied_request = copy.copy(request_session['pages'])
    copied_request.update(entry_details)
    request_session['pages'] = copied_request
