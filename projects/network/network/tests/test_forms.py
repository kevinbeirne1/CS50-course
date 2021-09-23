import json
from datetime import datetime
from unittest import skip
from unittest.mock import Mock, patch

import pytz
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import TestCase
from django.utils import timezone

from ..forms import CreateUserForm, EditPostForm, NewPostForm
from ..models import Post
from .factories import PostFactory, UserFactory

User = get_user_model()


class CreateUserFormTest(TestCase):

    def test_valid_create_user_form_creates_user(self):
        """
        Verify that valid CreateUserForm creates instance of User
        """
        request = HttpRequest()
        request.POST = {
            'username': 'harry',
            'email': 'hpotter@test.com',
            'password1': 'P@ssword!',
            'password2': 'P@ssword!',
        }

        form = CreateUserForm(request.POST)
        form.save()

        user = User.objects.first()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, 'harry')

    def test_invalid_create_user_form_doesnt_create_user(self):
        """
        Verify that valid CreateUserForm creates instance of User
        """
        request = HttpRequest()
        request.POST = {}

        form = CreateUserForm(request.POST)
        with self.assertRaises(ValueError):
            form.save()

        self.assertEqual(User.objects.count(), 0)


class NewPostFormTest(TestCase):

    def setUp(self) -> None:
        self.user = UserFactory()
        self.pub_date = pytz.utc.localize(datetime(2021, 1, 1))

    def test_valid_form_data(self):
        """
        Verify that NewPostForm is valid when provided with content, creator, pub_date
        """
        form_data = {'content': 'A new post', 'creator': self.user, 'pub_date': self.pub_date}
        form = NewPostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_form_is_invalid(self):
        """
        Verify that NewPostForm invalid when no information provided
        """
        form = NewPostForm()
        self.assertFalse(form.is_valid())

    def test_missing_creator_field_is_invalid(self):
        """
        Verify that NewPostForm invalid when creator field isn't provided
        """
        form_data = {'content': 'A new post', 'pub_date': self.pub_date}
        form = NewPostForm(form_data)
        self.assertFalse(form.is_valid())

    def test_blank_content_field_form_is_invalid(self):
        """
        Verify that NewPostForm invalid when content field isn't provided
        """
        form_data = {'content': '', 'creator': self.user, 'pub_date': self.pub_date}
        form = NewPostForm(form_data)
        self.assertFalse(form.is_valid())

    def test_blank_date_field_form_is_valid(self):
        """
        Verify that NewPostForm is valid when content field isn't provided
        """

        form_data = {'content': 'A new post', 'creator': self.user}
        form = NewPostForm(form_data)
        self.assertTrue(form.is_valid())

    def test_blank_pub_date_field_defaults_to_timezone_now(self):
        """
        Verify that pub_date defaults to datetime.now when content field isn't provided
        """
        time_now = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        form_data = {'content': 'A new post', 'creator': self.user}
        NewPostForm(form_data).save()
        new_post = Post.objects.first()
        post_pub_date = new_post.pub_date.strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(post_pub_date, time_now)


    def test_all_form_fields_present(self):
        """
        Verify that NewPostForm has content, creator, pub_date fields
        """
        form = NewPostForm()
        expected_form_fields = ['content', 'creator', 'pub_date']
        actual_form_fields = form.fields

        self.assertEqual(len(expected_form_fields), len(actual_form_fields))

        for expected_field in expected_form_fields:
            with self.subTest():
                self.assertIn(expected_field, actual_form_fields)


class EditPostFormTest(TestCase):

    def setUp(self) -> None:
        self.user = UserFactory()
        PostFactory(creator=self.user)

    def test_valid_form_data(self):
        """
        Verify that EditPostForm is valid when provided with content, post_id & user
        """
        form_data = json.dumps({"post_id": 1, "content": "A new post"})
        form = EditPostForm(user=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_form_raises(self):
        """
        Verify that EditPostForm raises KeyError when no user provided
        """
        with self.assertRaises(KeyError):
            EditPostForm()

    def test_form_invalid_without_data(self):
        """
        Verify that EditPostForm invalid when no content or post_id
        provided
        """
        form = EditPostForm(user=self.user)
        self.assertFalse(form.is_valid())

    def test_form_invalid_without_post_id(self):
        """
        Verify that EditPostForm invalid when no post_id provided
        """
        form_data = json.dumps({'post_id': 1})
        form = EditPostForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_without_content(self):
        """
        Verify that EditPostForm invalid when no content provided
        """
        form_data = json.dumps({'content': "a new post"})
        form = EditPostForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())

    def test_all_form_fields_present(self):
        """
        Verify that EditPostForm has content field
        """
        form = EditPostForm(user=None)
        expected_form_fields = ['content']
        actual_form_fields = form.fields

        self.assertEqual(len(expected_form_fields), len(actual_form_fields))

        for expected_field in expected_form_fields:
            with self.subTest():
                self.assertIn(expected_field, actual_form_fields)

    def test_get_instance_returns_correct_post(self):
        """
        Verify that get_instance returns the correct instance of Post
        """
        post = PostFactory(creator=self.user)
        post_id = post.pk
        PostFactory.create_batch(2)

        form_data = json.dumps({"post_id": post_id, "content": "A new post"})
        form = EditPostForm(user=self.user, data=form_data)
        form_post = form.instance

        self.assertEqual(form_post, post)

    def test_parse_JSON_returns_correct_data(self):
        """
        Verify that form.data returns a dict of data
        """
        raw_data = {"post_id": 1, "content": "A new post"}
        form_data = json.dumps(raw_data)
        form = EditPostForm(user=self.user, data=form_data)

        self.assertEqual(form.data, raw_data)
