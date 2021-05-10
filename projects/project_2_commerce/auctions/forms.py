from django.forms import ModelForm

from .models import Bid, Listing


def is_valid_bid():
    pass


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['name', 'description', 'category', 'starting_bid', 'image']


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount', 'bidder', 'listing']
