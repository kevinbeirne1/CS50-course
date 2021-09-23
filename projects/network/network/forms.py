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

    def __init__(self, *args, **kwargs):
        """
        - user: request.user is passed to form in user, assigned to self.user
        - data passed to form in JSON format, parsed and reassigned
        to self.data
        - self.instance assigned

        """
        self.user = kwargs.pop('user')
        super(EditPostForm, self).__init__(*args, **kwargs)
        try:
            self.data = self.parse_json_data()
            self.instance = self.get_instance()
        except (TypeError, models.Post.DoesNotExist, KeyError):
            self.is_bound = None

    def parse_json_data(self):
        """Parse the data in JSON format to python format"""
        return json.loads(self.data)

    def get_instance(self):
        """Get the Post instance from the post_id passed in self.data"""
        post_id = self.data["post_id"]
        return models.Post.objects.get(id=post_id, creator=self.user)

    class Meta:
        model = models.Post
        fields = [
            'content'
        ]