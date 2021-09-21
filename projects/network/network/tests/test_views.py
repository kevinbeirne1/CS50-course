import copy
import json
import re
import unittest
from unittest import skip
from unittest.mock import MagicMock, Mock, patch

import pytz
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.http import HttpRequest, HttpResponseRedirect
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape

from ..forms import CreateUserForm
from ..models import Post
from ..views import (LOGIN_FAILURE_MESSAGE, LOGIN_SUCCESS_MESSAGE,
                     LOGOUT_SUCCESS_MESSAGE, REGISTER_SUCCESS_MESSAGE)
from .factories import PostFactory, UserFactory

User = get_user_model()


def get_status_messages_from_response(response):
    request = response.wsgi_request
    return list(get_messages(request))


class IndexViewTest(TestCase):

    def tearDown(self) -> None:
        super().tearDown()
        PostFactory.reset_sequence()

    def test_index_url(self):
        """
        Verify that index url is '/'
        """
        url = reverse('network:index')
        self.assertEqual(url, '/')

    def test_index_returns_correct_html(self):
        """
        Verify that index uses 'network/index.html' template
        """
        response = self.client.get(reverse('network:index'))
        self.assertTemplateUsed(response, "network/index.html")

    def test_post_instances_are_passed_to_index_template(self):
        """
        Verify that Post instances are passed to 'network/index.html'
        """

        PostFactory()
        response = self.client.get(reverse('network:index'))

        response_objects = response.context['object_list']
        self.assertIsInstance(response_objects[0], Post)

    def test_post_instances_passed_in_reverse_chronological_order(self):
        """
        Verify that Post instances are passed in reverse chronological
        order to IndexView
        """

        response = self.client.get(reverse('network:index'))

        response_objects = response.context['object_list']
        pub_dates = [post.pub_date for post in response_objects]
        sorted_pub_dates = sorted(pub_dates, reverse=True)

        self.assertEqual(pub_dates, sorted_pub_dates)

    def test_pagination_passed_to_index_template(self):
        """
        Verify that Posts are paginated in groups of 10
        :return:
        """
        PostFactory.create_batch(11)
        response = self.client.get(reverse('network:index'))
        pagination_status = response.context['is_paginated']

        self.assertTrue(pagination_status)

        paginated_posts = response.context['page_obj']
        self.assertEqual(len(paginated_posts), 10)


class RegisterViewTest(TestCase):

    def test_register_url(self):
        """
        Verify that register url is '/register/'
        """
        url = reverse('network:register')
        self.assertEqual(url, '/register/')

    def test_register_returns_correct_html(self):
        """Verify that '/register' uses 'network/register.html' template"""
        response = self.client.get(reverse('network:register'))
        self.assertTemplateUsed(response, 'network/register.html')

    def test_register_can_save_a_new_user_account(self):
        """Verify that '/register' creates a new user in the database"""
        self.client.post(reverse('network:register'), data={
            'username': 'harry',
            'email': 'hpotter@test.com',
            'password1': 'P@ssword!',
            'password2': 'P@ssword!',
        })

        new_user = User.objects.first()

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(new_user.username, 'harry')

    def test_successful_register_redirects_to_index(self):
        """
        Verify that '/register' redirects to the index page after valid post data
        """
        response = self.client.post(reverse('network:register'), data={
            'username': 'harry',
            'email': 'hpotter@test.com',
            'password1': 'P@ssword!',
            'password2': 'P@ssword!',
        })
        self.assertRedirects(response, reverse('network:index'))

    def test_successful_register_logs_in_user(self):
        """
        Verify that '/register' logs in user after valid post data
        """
        response = self.client.post(reverse('network:register'), data={
            'username': 'harry',
            'email': 'hpotter@test.com',
            'password1': 'P@ssword!',
            'password2': 'P@ssword!',
        })
        request = response.wsgi_request
        user = request.user
        self.assertTrue(user.is_authenticated)

    def test_for_invalid_input_renders_register_template(self):
        """
        Verify that no data post to '/register' that it stays on '/register
        """
        response = self.client.post(reverse('network:register'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/register.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post(reverse('network:register'))
        self.assertIsInstance(response.context['form'], CreateUserForm)

    def test_register_passes_error_message_if_no_password_match(self):
        """
        Verify that register passes an error messages to response
        when password and confirmation of password don't match
        """
        response = self.client.post(reverse('network:register'), data={
            'username': 'harry',
            'email': 'hpotter@test.com',
            'password1': 'P@ssword!',
            'password2': 'P@ssword',
        })
        self.assertContains(response, escape("The two password fields didn’t match."))

    def test_register_passes_error_message_if_duplicate_username(self):
        """
        Verify that register passes an error messages to response
        when username already exists
        """
        user = UserFactory(username='harry')
        response = self.client.post(reverse('network:register'), data={
            'username': 'harry',
            'email': 'hpotter@test.com',
            'password1': 'P@ssword!',
            'password2': 'P@ssword',
        })
        self.assertContains(response, escape("A user with that username already exists."))

    def test_register_passes_success_message(self):
        """
        Verify that register passes success messages to when account
        created
        """
        response = self.client.post(reverse('network:register'), data={
            'username': 'harry',
            'email': 'hpotter@test.com',
            'password1': 'P@ssword!',
            'password2': 'P@ssword!',
        })

        messages = get_status_messages_from_response(response)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), REGISTER_SUCCESS_MESSAGE)

    def test_logged_in_user_cannot_access_register(self):
        """
        Verify that a logged in user is redirects to '/' when trying to access
        register
        """
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get(reverse('network:register'))
        self.assertRedirects(response, reverse('network:index'))


class LoginViewTest(TestCase):

    def test_login_url(self):
        """
        Verify that login url is '/login/'
        """
        url = reverse('network:login')
        self.assertEqual(url, '/login/')

    def test_login_returns_correct_html(self):
        """Verify that LoginView uses 'network/login.html' template"""
        response = self.client.get(reverse('network:login'))
        self.assertTemplateUsed(response, 'network/login.html')

    def test_invalid_login_passes_error_message(self):
        """
        Verify invalid LoginView POST passes error message
        """
        UserFactory(username='harry')

        response = self.client.post(reverse('network:login'), data={
            'username': 'harry',
            'password': 'pass',
        })
        self.assertContains(response, escape(LOGIN_FAILURE_MESSAGE))

    def test_for_invalid_login_renders_login_template(self):
        """
        Verify invalid LoginView POST renders network/login.html
        """
        response = self.client.post(reverse('network:login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/login.html')

    def test_valid_login_passes_success_message(self):
        """
        Verify valid LoginView POST passes success message
        """
        UserFactory(username='harry')

        response = self.client.post(reverse('network:login'), data={
            'username': 'harry',
            'password': 'P@ssword!',
        })
        messages = get_status_messages_from_response(response)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), LOGIN_SUCCESS_MESSAGE)

    def test_valid_login_redirects_to_index(self):
        """
        Verify valid LoginView POST redirects to index
        """
        UserFactory(username='harry')

        response = self.client.post(reverse('network:login'), data={
            'username': 'harry',
            'password': 'P@ssword!',
        })
        self.assertRedirects(response, reverse('network:index'))

    def test_valid_login_logs_in_user(self):
        """
        Verify valid LoginView POST logs in the user
        """
        UserFactory(username='harry')

        response = self.client.post(reverse('network:login'), data={
            'username': 'harry',
            'password': 'P@ssword!',
        })
        request = response.wsgi_request

        self.assertTrue(request.user.is_authenticated)


class LogoutViewTest(TestCase):

    def setUp(self) -> None:
        self.user = UserFactory()
        self.client.force_login(self.user)

    def test_logout_url(self):
        """
        Verify that logout url is '/logout'
        """
        url = reverse('network:logout')
        self.assertEqual(url, '/logout')

    def test_logout_redirects_to_index(self):
        """
        Verify that LogoutView redirects to index
        """
        response = self.client.get(reverse('network:logout'))
        self.assertRedirects(response, reverse('network:index'))

    def test_logout_logs_out_user(self):
        """
        Verify that LogoutView logs out the user
        """
        response = self.client.get(reverse('network:logout'))
        request = response.wsgi_request

        self.assertFalse(request.user.is_authenticated)

    def test_logout_passes_success_message(self):
        """
        Verify LogoutView passes a logout successful message
        """
        response = self.client.post(reverse('network:logout'))
        messages = get_status_messages_from_response(response)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), LOGOUT_SUCCESS_MESSAGE)


class NewPostViewTest(TestCase):

    def setUp(self) -> None:
        """
        Create user instance and force login
        """
        self.user = UserFactory()
        self.client.force_login(self.user)

    def test_new_post_url(self):
        """
        Verify that new_post url is '/new_post/'
        """
        url = reverse('network:new_post')
        self.assertEqual(url, '/new_post/')

    def test_new_post_renders_correct_html(self):
        """
        Verify that NewPostView uses 'network/new_post.html' template
        """
        response = self.client.get(reverse('network:new_post'))
        self.assertTemplateUsed(response, "network/new_post.html")

    def test_invalid_new_post_POST_doesnt_create_post_model(self):
        """
        Verify that invalid NewPostView POST doesn't create instance of Post
        """
        self.client.post(reverse('network:new_post'))
        self.assertEqual(Post.objects.count(), 0)

    def test_for_invalid_new_post_renders_new_post_template(self):
        """
        Verify that invalid NewPostView POST renders network/new_post.html
        """
        response = self.client.post(reverse('network:new_post'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/new_post.html')

    def test_unauthenticated_user_cannot_GET_new_post(self):
        """
        Verify that a logged out user cannot access '/new_post/'
        """
        self.client.logout()
        response = self.client.get(reverse('network:new_post'))

        self.assertRedirects(response, reverse('network:index'))

    def test_unauthenticated_user_cannot_POST_to_new_post(self):
        """Verify that a logged out user cannot create instance of Post"""
        self.client.logout()
        self.client.post(reverse('network:new_post'), data={
            "content": "A new post"
        })

        self.assertEqual(Post.objects.count(), 0)

    def test_valid_new_post_creates_post(self):
        """Verify that a logged in user can create instance of Post"""
        date = timezone.now()

        self.client.post(reverse('network:new_post'), data={
            "content": "A new post",
            "creator": self.user.id,
            "pub_date": date,
        })
        new_post = Post.objects.first()

        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(new_post.content, "A new post")
        self.assertEqual(new_post.pub_date, date)

    def test_valid_new_post_redirects_to_index(self):
        """Verify that valid NewPostView POST redirects to index"""
        response = self.client.post(reverse('network:new_post'), data={
            "content": "A new post",
            "creator": self.user.id,
        })
        self.assertRedirects(response, reverse('network:index'))


class ProfileViewTest(TestCase):

    def setUp(self, *args, **kwargs) -> None:
        super().setUp(*args, **kwargs)
        self.user = UserFactory(username='harry')

    def tearDown(self) -> None:
        super().tearDown()
        PostFactory.reset_sequence()

    def test_profile_url(self):
        """
        Verify that profile url is '/<profile_name>/'
        """
        url = reverse('network:profile', kwargs={
            'profile_name': 'profile_name',
        })
        self.assertEqual(url, '/profile_name/')

    def test_profile_returns_correct_html(self):
        """
        Verify that ProfileView uses 'network/profile.html' template
        """
        response = self.client.get(reverse('network:profile', kwargs={
            'profile_name': 'harry',
        }))
        self.assertTemplateUsed(response, "network/profile.html")


    def test_post_instances_are_passed_to_profile_template(self):
        """
        Verify that Post instances are passed to 'network/profile.html'
        """

        PostFactory(creator=self.user)
        response = self.client.get(reverse('network:profile', kwargs={
            'profile_name': 'harry'
        }))

        response_objects = response.context['object_list']
        self.assertIsInstance(response_objects[0], Post)

    def test_only_profile_name_instances_are_passed_to_profile_template(self):
        """
        Verify that Post instances by <profile_name> are passed to
        'network/profile.html'
        """

        PostFactory.create_batch(2, creator=self.user)
        PostFactory()

        response = self.client.get(reverse('network:profile', kwargs={
            'profile_name': 'harry'
        }))

        response_objects = response.context['object_list']
        self.assertEqual(len(response_objects), 2)

    def test_post_instances_passed_in_reverse_chronological_order(self):
        """
        Verify that Post instances are passed in reverse chronological
        order to ProfileView
        """
        PostFactory(creator=self.user, content="A new post")
        PostFactory(creator=self.user, content="A second post")

        response = self.client.get(reverse('network:profile', kwargs={
            'profile_name': 'harry'
        }))

        response_objects = response.context['object_list']
        first_post = response_objects[0].content
        second_post = response_objects[1].content

        self.assertEqual(first_post, "A second post")
        self.assertEqual(second_post, "A new post")

    def test_pagination_passed_to_profile_template(self):
        """
        Verify that Posts are paginated in groups of 10
        """
        PostFactory.create_batch(11, creator=self.user)
        response = self.client.get(reverse('network:profile', kwargs={
            'profile_name': 'harry'
        }))
        pagination_status = response.context['is_paginated']

        self.assertTrue(pagination_status)

        paginated_posts = response.context['page_obj']
        self.assertEqual(len(paginated_posts), 10)

class FollowingViewTest(TestCase):

    def setUp(self, *args, **kwargs) -> None:
        super().setUp(*args, **kwargs)
        self.user = UserFactory()
        self.test_user = UserFactory(username='test_user')
        PostFactory.create_batch(2, creator=self.test_user)
        PostFactory()
        self.user.following.add(self.test_user)

    def tearDown(self) -> None:
        super().tearDown()
        PostFactory.reset_sequence()

    def test_following_url(self):
        """
        Verify that following url is '/following/'
        """
        url = reverse('network:following')
        self.assertEqual(url, '/following/')

    def test_following_returns_correct_html(self):
        """
        Verify that following uses 'network/following.html' template
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('network:following'))
        self.assertTemplateUsed(response, "network/following.html")

    def test_post_instances_are_passed_to_following_template(self):
        """
        Verify that Post instances are passed to 'network/following.html'
        """
        self.client.force_login(self.user)

        response = self.client.get(reverse('network:following'))

        response_objects = response.context['object_list']
        self.assertIsInstance(response_objects[0], Post)

    def test_logged_out_user_cannot_access_following(self):
        """
        Verify that a logged out user redirects to 'login' when trying to
        access following
        """

        response = self.client.get(reverse('network:following'))
        self.assertRedirects(response, reverse('network:login'))

    def test_logged_out_user_gets_error_message(self):
        """
        Verify error message is passed to template when anonymous
        tries to access
        """

        response = self.client.get(reverse('network:following'))
        messages = get_status_messages_from_response(response)

        login_required_message = "Login Required"
        self.assertEqual(str(messages[0]), login_required_message)

    def test_only_following_instances_are_passed_to_following_template(self):
        """
        Verify that Post instances followed by the user are passed to
        'network/following.html'
        """
        self.client.force_login(self.user)

        response = self.client.get(reverse('network:following'))
        response_objects = response.context['object_list']
        self.assertEqual(len(response_objects), 2)

    def test_post_instances_passed_in_reverse_chronological_order(self):
        """
        Verify that Post instances are passed in reverse chronological
        order to FollowingView
        """

        self.client.force_login(self.user)
        response = self.client.get(reverse('network:following'))

        response_objects = response.context['object_list']
        pub_dates = [post.pub_date for post in response_objects]
        sorted_pub_dates = sorted(pub_dates, reverse=True)

        self.assertEqual(pub_dates, sorted_pub_dates)

    def test_pagination_passed_to_profile_template(self):
        """
        Verify that Posts are paginated in groups of 10
        """
        PostFactory.create_batch(11, creator=self.test_user)
        self.client.force_login(self.user)

        response = self.client.get(reverse('network:following'))
        pagination_status = response.context['is_paginated']

        self.assertTrue(pagination_status)

        paginated_posts = response.context['page_obj']
        self.assertEqual(len(paginated_posts), 10)


class EditPostViewTest(TestCase):

    def test_edit_post_url(self):
        """
        Verify that edit_post url is '/edit_post/<post_id>'
        """
        url = reverse('network:edit_post')
        self.assertEqual(url, '/edit_post')

    def test_GET_edit_post_redirect_to_index(self):
        """
        Verify that user redirected to 'index' when trying
        to access edit_post with get request
        """
        self.client.force_login(UserFactory())
        response = self.client.get(reverse('network:edit_post'))
        self.assertRedirects(response, reverse('network:index'))

    def test_unauthenticated_user_cannot_PUT_edit_post(self):
        """
        Verify that an anonymous User cannot PUT to edit post
        """
        PostFactory()

        self.client.put(
            reverse('network:edit_post'),
            json.dumps({"post_id": 1, "content": "A new post"}),
            content_type='application/json'
        )

        post = Post.objects.first()
        self.assertNotEqual(post.content, "A new post")

    def test_unauthenticated_user_edit_post_PUT_redirects_to_index(self):
        """
        Verify that an anonymous User redirected to index when PUT request
        to edit post
        """
        PostFactory()

        response = self.client.put(
            reverse('network:edit_post'),
            json.dumps({"post_id": 1, "content": "A new post"}),
            content_type='application/json'
        )

        self.assertRedirects(response, reverse('network:index'))

    # @skip
    def test_user_cannot_PUT_edit_post_on_others_posts(self):
        """
        Verify that a logged in User cannot PUT edit post on
        another persons post
        """
        PostFactory()
        self.client.force_login(UserFactory())

        self.client.put(
            reverse('network:edit_post'),
            json.dumps({"post_id": 1, "content": "A new post"}),
            content_type='application/json'
        )

        post = Post.objects.first()
        self.assertNotEqual(post.content, "A new post")

    # @skip
    def test_user_edit_post_PUT_redirects_to_index_on_others_posts(self):
        """
        Verify that a logged in User redirected to index when PUT
        request to edit post on another users post
        """
        PostFactory()
        self.client.force_login(UserFactory())

        response = self.client.put(
            reverse('network:edit_post'),
            json.dumps({"post_id": 1, "content": "A new post"}),
            content_type='application/json'
        )

        self.assertRedirects(response, reverse('network:index'))

    def test_valid_edit_post_PUT_doesnt_redirect(self):
        """
        Verify that there is no redirect when POST request
        to edit_post
        """
        PostFactory()
        test_user = User.objects.first()
        self.client.force_login(test_user)

        response = self.client.put(
            reverse('network:edit_post'),
            json.dumps({"post_id": 1, "content": "A new post"}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 204)

    def test_valid_PUT_edit_post_updates_post(self):
        """
        Verify that a valid POST request to edit_post updates
        Post instance
        """
        PostFactory()
        test_user = User.objects.first()
        self.client.force_login(test_user)

        self.client.put(
            reverse('network:edit_post'),
            json.dumps({"post_id": 1, "content": "A new post"}),
            content_type='application/json'
        )

        new_post = Post.objects.first()

        self.assertEqual(new_post.content, "A new post")

