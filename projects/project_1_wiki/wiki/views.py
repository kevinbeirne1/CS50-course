from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
import random

from . import forms
import markdown2


app_name = "wiki"

pages = {"Hello": "world", "Monty": "pyt<i>hon</i>", "Hel1lo1": "world",
         "Hello2": "world", "Hel3ello3": "world"}

# in time replace pages with request.session


def index(request):
    if 'pages' not in request.session:
        request.session['pages'] = []
    return render(request, f"{app_name}/index.html", {
        "pages": request.session['pages'],
        "title": 'Homepage',
        "search_form": forms.SearchForm(),
        "markdown": u"<i>italicised</i>"
    })


def entry(request, entry_name):
    entry_name = entry_name.capitalize()
    if entry_name not in request.session['pages']:
        return error_page(request)
    return render(request, f"{app_name}/entry.html", {
        "entry_name": entry_name,
        "entry_markdown": markdown2.markdown(pages[entry_name]),
        "search_form": forms.SearchForm(),
    })


def search(request):
    search_name = request.GET["search_name"].capitalize()
    partial_matches = []
    for page in pages:
        if search_name == page:
            return HttpResponseRedirect(f"/{app_name}/{search_name}")
        elif search_name in page:
            partial_matches.append(page)
    # return HttpResponse(partial_matches)
    return render(request, f"{app_name}/search.html", {
        "search_name": forms.SearchForm(initial={"search_name": search_name}),
        "partial_matches": partial_matches,
        "search_form": forms.SearchForm(),
    })


def old_search(request):
    if request.method == "POST":
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            search_name = form.cleaned_data['search_name']
            partial_matches = []
            for page in pages:

                if search_name == page:
                    return HttpResponseRedirect(f"/{app_name}/{search_name}")
                elif search_name in page:
                    partial_matches.append(page)
            return render(request, f"{app_name}/search.html", {
                "form": form,
                "partial_matches": partial_matches,
                "search_form": forms.SearchForm(),
            })
    return render(request, f"{app_name}/search.html", {
        "form": forms.SearchForm(),
        "search_form": forms.SearchForm(),
    })

    return render(request, f"{app_name}/search.html", {
        "form": forms.SearchForm(),
        "partial_matches": partial_matches,
        "search_form": forms.SearchForm(),
        # "search_name": search_name,
        # "title": f"{search_name} - Search"
    })


def new_page(request):
    if request.method == "POST":
        form = forms.NewEntryForms(request.POST)
        if form.is_valid():
            entry_name = form.cleaned_data['entry_name']
            entry_markdown = form.cleaned_data['entry_markdown']
            pages[entry_name] = entry_markdown
            return HttpResponseRedirect(f"/{app_name}/{entry_name}")

        else:
            return render(request, "wiki/new_page.html", {
                "form": forms.NewEntryForms(),
                "search_form": forms.SearchForm(),
            })

    return render(request, "wiki/new_page.html", {
        "form": forms.NewEntryForms(),
        "search_form": forms.SearchForm(),
    })


def edit_page(request):
    # name_of_page_to_edit = "Monty"
    if request.method == "POST":
        form = forms.NewEntryForms(request.POST)

        if form.is_valid():
            entry_name = form.cleaned_data["entry_name"]
            entry_markdown = form.cleaned_data["entry_markdown"]
            pages[entry_name] = entry_markdown
            return HttpResponseRedirect(f"/{app_name}/{entry_name}")

        else:
            entry_name = form.cleaned_data["entry_name"]
            return render(request, f"{app_name}/edit_page.html", {
                "entry_name": entry_name,
                "entry_markdown": pages[entry_name],
                "search_form": forms.SearchForm(),
            })


def error_page(request):
    return render(request, f"{app_name}/error_page.html", {
        "title": "Error Page",
        "search_form": forms.SearchForm(),
    })


def random_page(request):
    chosen_page = random.choice(list(pages))
    return redirect(f"/{app_name}/{chosen_page}")