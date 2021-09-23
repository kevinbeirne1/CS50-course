import json
import logging

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db.models import Model

from . import models


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = models.User
        fields = [
            "username",
            "email",
        ]


class NewPostForm(forms.ModelForm):

    pub_date = forms.DateTimeField(required=False)

    class Meta:
        model = models.Post
        fields = [
            'content',
            'creator',
            'pub_date'
        ]


class EditPostForm(forms.ModelForm):

    class Meta:
        model = models.Post
        fields = [
            'content'
        ]

class LikePostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.Post
        fields = [
            'likes'
        ]