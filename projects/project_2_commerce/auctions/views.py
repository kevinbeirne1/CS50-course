from datetime import datetime
import functools

from django.contrib.auth import authenticate, login, logout, decorators
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import BidForm, ListingForm
from .models import *


def verify_login(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        return func(request, *args, **kwargs)
    return wrapper


def index(request, message=''):
    return render(request, "auctions/index.html",{
        "active_listings": Listing.objects.exclude(active=False).all(),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful")
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid username and/or password")
            return render(request, "auctions/login.html")
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, "Passwords must match")
            return render(request, "auctions/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken.")
            return render(request, "auctions/register.html")
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@decorators.login_required
def create_listing_view(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            new_listing = form.save()
            # new_listing.creator = request.user
            # new_listing.save()
            messages.success(request, "Listing was created")
            return HttpResponseRedirect(reverse(
                'listing', kwargs={"listing_id": new_listing.id}))

        return HttpResponse("didn't new page")

    return render(request, "auctions/create.html", {
        "form": ListingForm(),
    })


def active_listings_view(request):
    return HttpResponseRedirect(reverse("index"))


def listing_view(request, listing_id):

    try:
        # Query listing_id, if none redirect to index
        current_listing = Listing.objects.get(id=listing_id)
        comments = current_listing.comments.all()
    except ObjectDoesNotExist:
        messages.error(request, "Listing doesn't exist")
        return HttpResponseRedirect(reverse('index'))

    if request.user.is_authenticated:
        # If logged in, query watchlist
        in_watchlist = Watchlist.objects.filter(user=request.user, item=listing_id).exists()
        users_watchlist = Watchlist.objects.get(user=request.user)
    else:
        in_watchlist = None

    if request.method == "POST":
        # Check if adding/removing from watchlist
        if add_remove := request.POST.get("add_remove", ""):
            users_watchlist.add_remove_item(listing_id, add_remove)

        # Read submitted bid and place if valid
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            new_bid = bid_form.save(commit=False)
            if current_listing.place_bid(new_bid):
                messages.success(request, "bid was placed")
            else:
                messages.error(request, "bid was too low")

        return HttpResponseRedirect(reverse("listing", kwargs={
            "listing_id":listing_id
        }))

    return render(request, "auctions/listing.html", {
        "listing": current_listing,
        "comments": comments,
        "in_watchlist": in_watchlist,
        "bid_form": BidForm,
    })


@decorators.login_required
def watchlist_view(request, user_id):
    watchlist_owner = User.objects.get(id=user_id)
    if watchlist_owner == request.user:
        try:
            watchlist = Watchlist.objects.get(user=watchlist_owner)
        except ObjectDoesNotExist:
            watchlist = ""

        return render(request, "auctions/watchlist.html", {
            "owner": watchlist_owner,
            "watchlist": watchlist,
        })
    else:
        messages.error(request, "Login to view your watchlist")
        return HttpResponseRedirect(reverse('index'))


def categories_view(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
    "categories": categories
    })

def specific_category_view(request, category_id):
    category_items = Listing.objects.filter(category=category_id)
    # category_name = Category.objects.get(category_id).name
    return render(request, "auctions/specific_category.html", {
        "category_items": category_items,
        # "category_name": category_name,
    })


def close_listing(request, listing_id):
    if request.method == "POST":
        current_listing = Listing.objects.get(id=listing_id)
        current_listing.active = False
        current_listing.save()
        messages.success(request, "This listing has been closed")

    return HttpResponseRedirect(reverse(
        "listing",
        kwargs={"listing_id":listing_id}
    ))


def add_comment(request, listing_id):
    if request.method == "POST":
        # listing_id = request.POST['listing_id']
        comment = request.POST['comment']
        # user = request.user
        listing = Listing.objects.get(id=listing_id)
        new_comment = Comment(detail=comment, listing=listing, commenter=request.user)
        new_comment.save()
    return HttpResponseRedirect(reverse(
        "listing",
        kwargs={"listing_id": listing_id}
    ))



