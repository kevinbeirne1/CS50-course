import copy
from unittest import skip
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.http import HttpRequest
from django.test import RequestFactory, TestCase
from django.utils.html import escape

from ..forms import CreateUserForm
from ..views import (LOGIN_SUCCESS_MESSAGE, LOGOUT_SUCCESS_MESSAGE,
                     REGISTER_SUCCESS_MESSAGE)

User = get_user_model()


def get_status_messages_from_response(response):
    request = response.wsgi_request
    return list(get_messages(request))


class IndexViewTest(TestCase):
    pass


class RegisterViewTest(TestCase):

    def test_register_returns_correct_html(self):
        """Verify that '/register' uses 'network/register.html' template"""
        response = self.client.get('/register')
        self.assertTemplateUsed(response, 'network/register.html')

    def test_register_can_save_a_new_user_account(self):
        """Verify that '/register' creates a new user in the database"""
        self.client.post('/register', data={
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
        response = self.client.post('/register', data={
            'username': 'harry',
            'email': 'hpotter@test.com',
            'password1': 'P@ssword!',
            'password2': 'P@ssword!',
        })
        self.assertRedirects(response, "/")

    def test_successful_register_logs_in_user(self):
        """
        Verify that '/register' logs in user after valid post data
        """
        response = self.client.post('/register', data={
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
        response = self.client.post('/register')
        self.assertURLEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/register.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/register')
        self.assertIsInstance(response.context['form'], CreateUserForm)

    def test_register_passes_error_message_if_no_password_match(self):
        """
        Verify that register passes an error messages to response
        when password and confirmation of password don't match
        """
        response = self.client.post('/register', data={
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
        response = self.client.post('/register', data={
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
        response = self.client.post('/register', data={
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
        response = self.client.get('/register')
        self.assertRedirects(response, '/')


class LoginViewTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='harry',
            email='hpotter@test.com',
            password='P@ssword!',
        )

    def test_login_returns_login_html(self):
        """Verify that '/login' uses 'network/login.html' template"""
        response = self.client.get('/login')
        self.assertTemplateUsed(response, 'network/login.html')

    def test_invalid_login_passes_error_message(self):
        response = self.client.post('/login', data={
            'username': 'harry',
            'password': 'pass',
        })
        self.assertContains(response, escape("Invalid username and/or password"))

    def test_valid_login_passes_success_message(self):
        """
        Verify that login passes success messages to when user logs in
        """
        response = self.client.post('/login', data={
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
        response = self.client.post('/login', data={
            'username': 'harry',
            'password': 'P@ssword!',
        })
        self.assertRedirects(response, '/')

    def test_valid_login_logs_in_user(self):
        """
        Verify that successful login logs in the user
        """
        response = self.client.post('/login', data={
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

    def test_logout_redirects_to_index(self):
        """
        Verify that '/logout' redirects to index
        """
        response = self.client.get('/logout')
        self.assertRedirects(response, '/')

    def test_logout_logs_out_user(self):
        """
        Verify that '/logout' logs out the user
        """
        response = self.client.get('/logout')
        request = response.wsgi_request

        self.assertFalse(request.user.is_authenticated)

    def test_logout_passes_success_message(self):
        """
        Verify '/logout' passes a logout successful message
        """
        response = self.client.post('/logout')
        messages = get_status_messages_from_response(response)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), LOGOUT_SUCCESS_MESSAGE)



