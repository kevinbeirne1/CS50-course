import copy
from unittest import skip
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.http import HttpRequest
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils.html import escape

from ..forms import CreateUserForm
from ..models import Post
from ..views import (LOGIN_SUCCESS_MESSAGE, LOGOUT_SUCCESS_MESSAGE,
                     REGISTER_SUCCESS_MESSAGE)

User = get_user_model()


def get_status_messages_from_response(response):
    request = response.wsgi_request
    return list(get_messages(request))


class IndexViewTest(TestCase):

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
        Post.objects.create(text="A new post")
        response = self.client.get(reverse('network:index'))

        response_objects = response.context['object']
        self.assertIsInstance(response_objects[0], Post)


class RegisterViewTest(TestCase):

    def test_register_url(self):
        """
        Verify that register url is '/register'
        """
        url = reverse('network:register')
        self.assertEqual(url, '/register')

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
        User.objects.create_user(
            username='harry',
            email='hpotter@test.com',
            password='P@ssword!',
        )
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
        # request = response.wsgi_request
        # messages = list(get_messages(request))

        messages = get_status_messages_from_response(response)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), REGISTER_SUCCESS_MESSAGE)

    def test_logged_in_user_cannot_access_register(self):
        """
        Verify that a logged in user is redirects to '/' when trying to access
        register
        """
        user = User.objects.create_user(
            username='harry',
            email='hpotter@test.com',
            password='P@ssword!',
        )
        self.client.force_login(user)
        response = self.client.get(reverse('network:register'))
        self.assertRedirects(response, reverse('network:index'))


class LoginViewTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='harry',
            email='hpotter@test.com',
            password='P@ssword!',
        )

    def test_login_url(self):
        """
        Verify that login url is '/login'
        """
        url = reverse('network:login')
        self.assertEqual(url, '/login')

    def test_login_returns_correct_html(self):
        """Verify that '/login' uses 'network/login.html' template"""
        response = self.client.get(reverse('network:login'))
        self.assertTemplateUsed(response, 'network/login.html')

    def test_invalid_login_passes_error_message(self):
        response = self.client.post(reverse('network:login'), data={
            'username': 'harry',
            'password': 'pass',
        })
        self.assertContains(response, escape("Invalid username and/or password"))

    def test_for_invalid_login_renders_login_template(self):
        """
        Verify that invalid '/login' POST renders network/login.html
        """
        response = self.client.post(reverse('network:login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/login.html')

    def test_valid_login_passes_success_message(self):
        """
        Verify that login passes success messages to when user logs in
        """
        response = self.client.post(reverse('network:login'), data={
            'username': 'harry',
            'password': 'P@ssword!',
        })
        messages = get_status_messages_from_response(response)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), LOGIN_SUCCESS_MESSAGE)

    def test_valid_login_redirects_to_index(self):
        """
        Verify that successful login redirects to index
        """
        response = self.client.post(reverse('network:login'), data={
            'username': 'harry',
            'password': 'P@ssword!',
        })
        self.assertRedirects(response, reverse('network:index'))

    def test_valid_login_logs_in_user(self):
        """
        Verify that successful login logs in the user
        """
        response = self.client.post(reverse('network:login'), data={
            'username': 'harry',
            'password': 'P@ssword!',
        })
        request = response.wsgi_request

        self.assertTrue(request.user.is_authenticated)


class LogoutViewTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='harry',
            email='hpotter@test.com',
            password='P@ssword!',
        )
        self.client.force_login(self.user)

    def test_logout_url(self):
        """
        Verify that logout url is '/logout'
        """
        url = reverse('network:logout')
        self.assertEqual(url, '/logout')


    def test_logout_redirects_to_index(self):
        """
        Verify that '/logout' redirects to index
        """
        response = self.client.get(reverse('network:logout'))
        self.assertRedirects(response, reverse('network:index'))

    def test_logout_logs_out_user(self):
        """
        Verify that '/logout' logs out the user
        """
        response = self.client.get(reverse('network:logout'))
        request = response.wsgi_request

        self.assertFalse(request.user.is_authenticated)

    def test_logout_passes_success_message(self):
        """
        Verify '/logout' passes a logout successful message
        """
        response = self.client.post(reverse('network:logout'))
        messages = get_status_messages_from_response(response)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), LOGOUT_SUCCESS_MESSAGE)


class NewPostViewTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='harry',
            email='hpotter@test.com',
            password='P@ssword!',
        )
        self.client.force_login(self.user)

    def test_new_post_url(self):
        """
        Verify that new_post url is '/new_post'
        """
        url = reverse('network:new_post')
        self.assertEqual(url, '/new_post')

    def test_new_post_renders_correct_html(self):
        """
        Verify that '/new_post' uses 'network/new_post.html' template
        """
        response = self.client.get(reverse('network:new_post'))
        self.assertTemplateUsed(response, "network/new_post.html")

    def test_invalid_new_post_POST_doesnt_create_post_model(self):
        """
        Verify that invalid POST doesn't create instance of Post
        """
        self.client.post(reverse('network:new_post'))
        self.assertEqual(Post.objects.count(), 0)

    def test_for_invalid_login_renders_login_template(self):
        """
        Verify that invalid '/login' POST renders network/login.html
        """
        response = self.client.post('/new_post')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/new_post.html')

    def test_unauthenticated_user_cannot_GET_new_post(self):
        """
        Verify that a logged out user cannot access '/new_post'
        """
        self.client.logout()
        response = self.client.get(reverse('network:new_post'))

        self.assertRedirects(response, reverse('network:index'))

    def test_unauthenticated_user_cannot_POST_to_new_post(self):
        """Verify that a logged out user cannot create instance of Post"""
        self.client.logout()
        self.client.post(reverse('network:new_post'), data={
            "text": "A new post"
        })

        self.assertEqual(Post.objects.count(), 0)

    def test_valid_new_post_creates_post(self):
        """Verify that a logged in user can create instance of Post"""

        response = self.client.post(reverse('network:new_post'), data={
            "text": "A new post"
        })

        new_post = Post.objects.first()

        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(new_post.text, "A new post")

    def test_valid_new_post_redirects_to_index(self):
        """Verify that a logged out user cannot create instance of Post"""
        response = self.client.post(reverse('network:new_post'), data={
            "text": "A new post"
        })
        self.assertRedirects(response, reverse('network:index'))

