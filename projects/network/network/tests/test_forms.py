from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import TestCase

from ..forms import CreateUserForm

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
