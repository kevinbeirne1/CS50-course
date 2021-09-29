from django import forms
from django.contrib.auth.forms import UserCreationForm

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
