from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Bid, Category, Comment, Listing, User, Watchlist


class BidAdmin(admin.ModelAdmin):
    list_filter = ['listing', 'bidder']
    list_display = ['listing', 'bidder', 'amount',]


class CategoryAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     ("Info", {"fields": ['listing']}) ,
    #     ("Commenters", {"fields": ['commenter']}),
    # ]
    list_filter = ['listing', 'commenter']
    list_display = ("listing", "commenter", "detail", "comment_date" )


class ListingAdmin(admin.ModelAdmin):
    list_filter = ['active', "category" ]
    list_display = ( "__str__", "category","creator", "pub_date", "active", )


class WatchlistAdmin(admin.ModelAdmin):
    pass


admin.site.register(Bid, BidAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Watchlist, WatchlistAdmin)