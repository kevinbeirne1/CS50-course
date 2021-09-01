from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import Post


class PostModelTest(TestCase):

    def test_empty_text_field(self):
        """
        Verify that validation error is raised if no text field provided
        """
        post = Post()
        with self.assertRaises(ValidationError):
            post.full_clean()

