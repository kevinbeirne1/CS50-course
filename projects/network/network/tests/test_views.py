import copy
from unittest import skip

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import RequestFactory, TestCase

from ..views import register

User = get_user_model()


def get_status_messages_from_response(response):
    request = response.wsgi_request
    return list(get_messages(request))


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
            'password': 'password',
            'confirmation': 'password',
        })

        new_user = User.objects.first()

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(new_user.username, 'harry')

    def test_register_passes_success_message(self):
        """
        Verify that register passes success messages to when account
        created
        """
        response = self.client.post('/register', data={
            'username': 'harry',
            'email': 'hpotter@test.com',
            'password': 'password',
            'confirmation': 'password',
        })
        # request = response.wsgi_request
        # messages = list(get_messages(request))

        messages = get_status_messages_from_response(response)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "New Account Created")

    def test_redirects_to_register_if_no_info_given(self):
        """
        Verify that no data post to '/register' that it redirects to '/register
        """
        response = self.client.post('/register')
        self.assertRedirects(response, '/register')

    def test_register_passes_error_message_if_no_info_given(self):
        """
        Verify that register passes an error message to response when
        no data entered
        """
        response = self.client.post('/register')

        messages = get_status_messages_from_response(response)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "All Boxes Are Required")

    def test_register_passes_error_message_if_no_password_match(self):
        """
        Verify that register passes an error messages to response
        when password and confirmation of password don't match
        """
        response = self.client.post('/register', data={
            'username': 'harry',
            'email': 'hpotter@test.com',
            'password': 'password',
            'confirmation': 'incorrect',
        })
        messages = get_status_messages_from_response(response)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Passwords Do Not Match")

    def test_register_passes_error_message_if_duplicate_username(self):
        """
        Verify that register passes an error messages to response
        when username already exists
        """
        User.objects.create_user(
            username='harry',
            email='hpotter@test.com',
            password='password',
        )
        response = self.client.post('/register', data={
            'username': 'harry',
            'email': 'hpotter@test.com',
            'password': 'password',
            'confirmation': 'password',
        })
        messages = get_status_messages_from_response(response)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username Already Taken")


class LoginViewTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='harry',
            email='hpotter@test.com',
            password='password',
        )

    def test_login_returns_correct_html(self):
        """Verify that '/login' uses 'network/login.html' template"""
        response = self.client.get('/login')
        self.assertTemplateUsed(response, 'network/login.html')

    def test_valid_login_passes_success_message(self):
        """
        Verify that login passes success messages to when user logs in
        """
        response = self.client.post('/login', data={
            'username': 'harry',
            'password': 'password',
        })
        messages = get_status_messages_from_response(response)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Log In Completed")


