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


class EditPostForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EditPostForm, self).__init__(*args, **kwargs)

    def clean(self):
        try:
            models.Post.objects.get(
                id=self.data['post_id'], creator=self.user
            )
        except (models.Post.DoesNotExist, TypeError):
            raise ValidationError('User cannot edit other persons post')
        return super(EditPostForm, self).clean()

    class Meta:
        model = models.Post
        fields = [
            'content'
        ]