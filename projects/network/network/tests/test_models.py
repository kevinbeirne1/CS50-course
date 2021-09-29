from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from ..models import Post
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
        post = PostFactory.build(creator=None)
        with self.assertRaises(ValidationError):
            post.full_clean()

    def test_empty_content_field(self):
        """
        Verify that validation error is raised if no content field provided
        """
        post = PostFactory.build(content="")
        with self.assertRaises(ValidationError):
            post.full_clean()

    def test_empty_date_field_defaults_to_timezone_now(self):
        """
        Verify that instance of Post is created when no date field provided and
        it defaults to timezone.now()
        """

        time_now = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        Post.objects.create(
            creator=UserFactory(username='harry'), content='A new post'
        )

        new_post = Post.objects.first()
        pub_date = new_post.pub_date.strftime("%Y-%m-%d %H:%M:%S")

        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(new_post.content, "A new post")
        self.assertEqual(new_post.creator.username, 'harry')
        self.assertEqual(pub_date, time_now)

    def test_can_create_post_instance(self):
        """
        Verify that instance of Post is created when provided with correct fields
        """
        PostFactory(content='Post #0')
        new_post = Post.objects.first()

        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(new_post.content, "Post #0")

    def test_content_max_length(self):
        """
        Verify that the max_length for content field is 160 characters
        """
        max_length = Post._meta.get_field('content').max_length
        self.assertEqual(max_length, 160)

    def test_Post_has_likes_as_many_to_many_field(self):
        """
        Verify that Post has a likes field
        """
        self.assertTrue(Post._meta.get_field('likes'))

    def test_Post_has_likes_count_property(self):
        """
        Verify that Post has a likes_count function that returns an integer
        """
        post = PostFactory()
        likes_count = post.likes_count
        self.assertEqual(likes_count, 0)

    def test_Post_like_count_can_be_incremented(self):
        """
        Verify that Post likes_count increments when a user likes Post
        """
        post = PostFactory()
        user = UserFactory()
        post.likes.add(user)

        likes_count = post.likes_count
        self.assertEqual(likes_count, 1)

    def test_Post_ordering_by_pub_date(self):
        """
        Verify that posts are ordered by pub_date in reverse chronological order
        """
        PostFactory(content='A new post')
        PostFactory(content='A second post')

        first_post = Post.objects.first()
        second_post = Post.objects.last()

        self.assertEqual(first_post.content, "A second post")
        self.assertEqual(second_post.content, 'A new post')
        self.assertTrue(first_post.pub_date > second_post.pub_date)


class UserModelTest(TestCase):

    def test_User_has_following_count_property(self):
        """
        Verify that User has a following property that returns an int
        """
        user = UserFactory()
        following_count = user.following_count
        self.assertEqual(following_count, 0)

    def test_following_count_can_be_incremented(self):
        """
        Verify that following_count increments when a user is followed
        """
        user = UserFactory()
        user.following.add(UserFactory())

        following_count = user.following_count

        self.assertEqual(following_count, 1)

    def test_following_increment_doesnt_change_followers_count(self):
        """
        Verify that followers_count doesnt increment when a user is
        followed
        """
        user = UserFactory()
        user.following.add(UserFactory())
        followers_count = user.followers_count

        self.assertEqual(followers_count, 0)

    def test_followers_count_can_be_incremented(self):
        """
        Verify that followers_count increments when a test_user follows
        the user
        """
        user = UserFactory()
        test_user = UserFactory(username='test_user')
        test_user.following.add(user)

        followers_count = user.followers_count

        self.assertEqual(followers_count, 1)

    def test_followers_increment_doesnt_change_following_count(self):
        """
        Verify that following_count doesnt increment when a test_user
        follows the user
        """
        user = UserFactory()
        test_user = UserFactory(username='test_user')
        test_user.following.add(user)

        following_count = user.following_count

        self.assertEqual(following_count, 0)

    def test_User_has_followers_count_property(self):
        """
        Verify that User has a followers property that returns an int
        """
        user = UserFactory()
        followers_count = user.followers_count
        self.assertEqual(followers_count, 0)
