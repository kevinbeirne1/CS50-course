from unittest import skip
from unittest.mock import MagicMock, Mock, patch

from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import Post, User
from .factories import PostFactory, UserFactory


class PostModelTest(TestCase):

    def test_cannot_save_empty_post(self, ):
        """
        Verify that validation error is raised if no fields
        """

        with self.assertRaises(ValidationError):
            Post().full_clean()

    def test_empty_user_field(self):
        """
        Verify that validation error is raised if no user field provided
        """
        post = PostFactory(content="")

        with self.assertRaises(ValidationError):
            post.full_clean()

    def test_empty_content_field(self):
        """
        Verify that validation error is raised if no content field provided
        """
        post = PostFactory.build(content="")
        # print(User.objects.first())
        with self.assertRaises(ValidationError):
            post.full_clean()

    def test_can_create_post_instance(self):
        """
        Verify that instance of Post is created when provided with correct fields
        """
        PostFactory()
        new_post = Post.objects.first()

        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(new_post.content, "A new post")
        self.assertEqual(new_post.creator.username, 'harry')

    def test_content_max_length(self):
        """
        Verify that the max_length for content field is 160 characters
        """
        max_length = Post._meta.get_field('content').max_length
        self.assertEqual(max_length, 160)

    # def test_field_specified(self):






