from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.admin.options import IS_POPUP_VAR, csrf_protect_m
from django.contrib.auth.admin import UserAdmin
from django.forms.forms import NON_FIELD_ERRORS
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text


from .models import Follow, Like, Post, User


class LikesAdmin(admin.ModelAdmin):
    list_filter = []
    list_display = ("id","post", "user", "like_unlike" )


class PostAdmin(admin.ModelAdmin):
    list_filter = []
    list_display = ("id", "creator", "content", "pub_date")


class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    list_display_links = ('user',)


admin.site.register(Follow, FollowAdmin)
admin.site.register(Like, LikesAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(User, UserAdmin)

