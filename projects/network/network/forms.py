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

    def __init__(self, *args, **kwargs):
        super(NewPostForm, self).__init__(*args, **kwargs)
        self.fields['pub_date'].required = False

    class Meta:
        model = models.Post
        fields = [
            'content',
            'creator',
            'pub_date'

        ]