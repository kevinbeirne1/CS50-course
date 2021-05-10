from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=300)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="creator")
    # category = models.CharField(max_length=40)
    category = models.ForeignKey(Category, on_delete=models.SET(1), related_name="categories")
    starting_bid = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    image = models.URLField(blank=True)
    pub_date = models.DateTimeField('listing date', default=timezone.now)

    class Meta:
        ordering = ['pub_date']

    @property
    def current_bid(self):
        return self.bids.order_by('-amount').first()

    @property
    def current_bid_amount(self):
        return self.current_bid.amount if self.current_bid else self.starting_bid

    def place_bid(self, new_bid):
        # Place submitted bid if higher than current bid
        if new_bid.amount > self.current_bid_amount:
            new_bid.save()
            return True
        return False

    def __str__(self):
        return f"#{self.pk} - {self.name}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='watching',
                             )
    item = models.ManyToManyField(Listing, related_name="watchers")

    # def in_watchlist(self):
    #     return self.item in self.item.all()

    def add_remove_item(self, listing, add_remove):
        if add_remove == "add":
            self.item.add(listing)
            message = "Added to watchlist"
        elif add_remove == "remove":
            self.item.remove(listing)
            message = "Removed from watchlist"

    def __str__(self):
        return f"{self.user}'s Watchlist - {[listing.name for listing in self.item.all()]}"


class Bid(models.Model):
    amount = models.PositiveIntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidding")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids", null=True)

    class Meta:
        ordering = ['-listing', '-amount']



    def __str__(self):
        return f"{self.bidder} bid ${self.amount} on item {self.listing}"


class Comment(models.Model):
    detail = models.CharField(max_length=300)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", default=None)
    commenter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="commenters")
    comment_date = models.DateTimeField('comment date', default=timezone.now)

    class Meta:
        ordering = ['-listing', 'comment_date']

    def __str__(self):
        return f"[{self.listing}] {self.pk}: - {self.detail[:30]}"

