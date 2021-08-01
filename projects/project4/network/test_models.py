from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone
import pytz
from unittest import mock

from .models import Like, Follow, Post, User


class PostTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Create Users & Posts"""
        for i, name in enumerate(["john", "mary", "paddy", "betty"], start=1):
            with mock.patch("django.utils.timezone.now") as mocked_time:
                mocked_time.return_value = pytz.utc.localize(datetime(2021, i, i))
                user = User.objects.create(username=name, email=f"{name}@email.com")
                Post.objects.create(creator=user, content=f"post-{i}", pub_date=timezone.now())

    # def setUp(self) -> None:
    #     """Create Users & Posts"""
    #     for i, name in enumerate(["john", "mary", "paddy", "betty"], start=1):
    #         with mock.patch("django.utils.timezone.now") as mocked_time:
    #             mocked_time.return_value = pytz.utc.localize(datetime(2021, i, i))
    #             user = User.objects.create(username=name, email=f"{name}@email.com")
    #             Post.objects.create(creator=user, content=f"post-{i}", pub_date=timezone.now())

    def test_content_max_length(self):
        """
        Verify that a post is max 160 Characters long
        """
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field("content").max_length
        self.assertEqual(max_length, 160)

    def test_no_likes_count(self):
        """
        Verify that likes count is 0 on a new post
        """
        post = Post.objects.get(id=1)
        likes_count = post.likes_count
        self.assertEqual(likes_count, 0)

    def test_likes_count_new_post(self):
        """
        Add likes to a new post and verify the likes count increases
        """
        post = Post.objects.get(id=1)
        users = [User.objects.get(id=i) for i in range(2, 5)]
        for i, user in enumerate(users, start=1):
            with self.subTest(f"Testing likes_count - #{i}"):
                Like.objects.create(post=post, user=user, like_unlike=True)
                likes_count = post.likes_count
                self.assertEqual(likes_count, i)

    def test_unlikes_count_new_post(self):
        """
        Add unlikes to a new post and verify the unlikes count increases
        """
        post = Post.objects.get(id=1)
        users = [User.objects.get(id=i) for i in range(2, 5)]
        for i, user in enumerate(users, start=1):
            with self.subTest(f"Testing unlikes_count - #{i}"):
                Like.objects.create(post=post, user=user, like_unlike=False)
                unlikes_count = post.unlikes_count
                self.assertEqual(unlikes_count, i)

    def test_likes_count_change_on_existing_post(self):
        """
        Add likes to a post with unlikes and verify that the likes_count and
        unlikes_count changes.
        """
        post = Post.objects.get(id=1)
        users = [User.objects.get(id=i) for i in range(2, 5)]
        # Create a like for each user
        for user in users:
            Like.objects.create(post=post, user=user, like_unlike=False)
        if post.unlikes_count != 3:
            raise Exception("Pre-test error - unlikes_count should equal 3")
        for i, user in enumerate(users, start=1):
            with self.subTest(f"Testing likes_count - #{i}"):
                Like.objects.filter(post=post, user=user).update(like_unlike=True)
                likes_count = post.likes_count
                unlikes_count = post.unlikes_count
                self.assertEqual(likes_count, i)
                self.assertEqual(unlikes_count, 3 - i)

    def test_likes_count_delete_like(self):
        """
        Delete likes on an existing post and verify that the likes_count
        decreases.
        """
        post = Post.objects.get(id=1)
        users = [User.objects.get(id=i) for i in range(2, 5)]
        for user in users:
            Like.objects.create(post=post, user=user, like_unlike=True)
        if post.likes_count != 3:
            raise Exception("Pre-test error - likes_count should equal 3")
        for i, user in enumerate(users, start=1):
            with self.subTest(f"Testing likes_count - #{i}"):
                Like.objects.filter(post=post, user=user).delete()
                likes_count = post.likes_count
                self.assertEqual(likes_count, 3 - i)

    def test_likes_count_delete_unlike(self):
        """
        Delete unlikes on an existing post and verify that the unlikes_count
        decreases.
        """
        post = Post.objects.get(id=1)
        users = [User.objects.get(id=i) for i in range(2, 5)]
        for user in users:
            Like.objects.create(post=post, user=user, like_unlike=False)
        if post.unlikes_count != 3:
            raise Exception("Pre-test error - unlikes_count should equal 3")
        for i, user in enumerate(users, start=1):
            with self.subTest(f"Testing likes_count - #{i}"):
                Like.objects.filter(post=post, user=user).delete()
                unlikes_count = post.unlikes_count
                self.assertEqual(unlikes_count, 3 - i)

    def test_object_name(self):
        """
        Verify __str__ method returns: '{post.id} - By {post.creator}'
        """
        post = Post.objects.get(id=1)
        expected_object_name = f"{post.id} - By {post.creator}"
        self.assertEqual(str(post), expected_object_name)

    def test_delete_user(self):
        """
        Verify that deleting a User from db deletes their posts
        """
        post = Post.objects.get(id=1)
        user = post.creator
        self.assertTrue(Post.objects.filter(creator=user).exists())
        user.delete()
        self.assertFalse(Post.objects.filter(creator=user).exists())

    def test_model_relation_no_information(self):
        """
        Verify error raised when saving Post with no information
        """
        post = Post()
        with self.assertRaises((ValidationError, ObjectDoesNotExist)):
            post.full_clean()

    def test_model_relation_creator_missing(self):
        """
        Verify error raised when saving Like without a creator value
        """
        post = Post(content="test", pub_date=datetime.now())
        with self.assertRaises(ValidationError):
            post.full_clean()

    def test_model_relation_content_missing(self):
        """
        Verify error raised when saving Like without a content value
        """
        post = Post(creator=User.objects.all()[0], pub_date=datetime.now())
        with self.assertRaises(ValidationError):
            post.full_clean()

    def test_model_relation_date_missing(self):
        """
        Verify pub_date defaults to timezone.now()when date isn't specified value
        """
        time_now = timezone.now()
        post = Post(creator=User.objects.all()[0], content="test")
        post.full_clean()
        post.save()
        self.assertEqual(time_now, post.pub_date)
        self.assertTrue(Post.objects.filter(id=post.id).exists())


class LikeTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        john = User.objects.create(username="john", email="john@email.com")
        User.objects.create(username="mary", email="mary@email.com")
        Post.objects.create(creator=john, content="post-1", pub_date=timezone.now())

    # def setUp(self) -> None:

    def test_cannot_like_post_multiple_times(self):
        """Verify user cannot like a post more than once"""
        post = Post.objects.get(id=1)
        user = User.objects.filter(id=post.creator.id).first()

        Like.objects.create(post=post, user=user, like_unlike=True)
        with self.assertRaises(IntegrityError):
            Like.objects.create(post=post, user=user, like_unlike=True)

    def test_cannot_like_own_post(self):
        """Verify user cannot like their own post"""
        post = Post.objects.get(id=1)
        with self.assertRaises(ValidationError, msg="Error should be raised if try to like your own post"):
            like = Like(post=post, user=post.creator, like_unlike=True)
            like.full_clean()

    def test_like_unlike_wording(self):
        """
        Verify like_unlike_wording() method returns:
        'like' if True
        'unlike' if False
        """
        post = Post.objects.get(id=1)
        user = User.objects.exclude(id=post.creator.id).first()
        like = Like(post=post, user=user)
        for test_case, expected in ((True, "like"), (False, "unlike")):
            with self.subTest(msg=f"Test like_unlike = {test_case}"):
                like.like_unlike = test_case
                actual = like.like_unlike_wording
                self.assertEqual(actual, expected)

    def test_object_name(self):
        """
        Verify __str__ method returns:
        'Post #{post.id} - {user} {like_unlike_wording}s this'
        """
        post = Post.objects.get(id=1)
        user = User.objects.exclude(id=post.creator.id).first()
        like = Like(post=post, user=user, like_unlike=True)
        actual = str(like)
        expected = f"Post #{post.id} - {user} {like.like_unlike_wording}s this"

        self.assertEqual(actual, expected)

    def test_model_relation_no_information(self):
        """
        Verify error raised when saving Like with no information
        """
        like = Like()
        with self.assertRaises((ObjectDoesNotExist, ValidationError)):
            like.full_clean()

    def test_model_relation_user_missing(self):
        """
        Verify error raised when saving Like without a user value
        """
        post = Post.objects.get(id=1)
        User.objects.exclude(id=post.creator.id).first()
        like = Like(post=post, like_unlike=True)
        with self.assertRaises(ObjectDoesNotExist):
            like.full_clean()

    def test_model_relation_post_missing(self):
        """
        Verify error raised when saving Like without a post value
        """
        post = Post.objects.get(id=1)
        user = User.objects.exclude(id=post.creator.id).first()
        like = Like(user=user, like_unlike=True)
        with self.assertRaises(ObjectDoesNotExist):
            like.full_clean()

    def test_model_relation_like_unlike_missing(self):
        """
        Verify error raised when saving Like without a like_unlike value
        """
        post = Post.objects.get(id=1)
        user = User.objects.exclude(id=post.creator.id).first()
        like = Like(user=user, post=post)
        with self.assertRaises(ValidationError):
            like.full_clean()

    def test_model_relation_like_unlike_missing_not_boolean(self):
        """
        Verify error raised when saving Like with non-boolean like_unlike value
        """
        post = Post.objects.get(id=1)
        user = User.objects.exclude(id=post.creator.id).first()
        like = Like(user=user, post=post, like_unlike=None)
        with self.assertRaises(ValidationError):
            like.full_clean()

    def test_model_relation(self):
        """
        Verify can save with user, post & like_unlike specified
        """
        post = Post.objects.get(id=1)
        user = User.objects.exclude(id=post.creator.id).first()
        like = Like(user=user, post=post, like_unlike=True)
        like.full_clean()
        like.save()
        self.assertEqual(Like.objects.all().count(), 1)

    def test_delete_post(self):
        """
        Verify that deleting a Post from db deletes its likes
        """
        post = Post.objects.get(id=1)
        user = User.objects.exclude(id=post.creator.id).first()
        Like.objects.create(user=user, post=post, like_unlike=True)
        self.assertTrue(Like.objects.filter(post=post).exists())
        post.delete()
        self.assertFalse(Like.objects.filter(post=post).exists())

    def test_delete_user(self):
        """
        Verify that deleting a User from db deletes its likes
        """
        post = Post.objects.get(id=1)
        user = User.objects.exclude(id=post.creator.id).first()
        Like.objects.create(user=user, post=post, like_unlike=True)
        self.assertTrue(Like.objects.filter(user=user).exists())
        post.delete()
        self.assertFalse(Like.objects.filter(user=user).exists())


class FollowTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        for i, name in enumerate(["john", "mary", "paddy", "betty", "tom"], start=1):
            with mock.patch("django.utils.timezone.now") as mocked_time:
                mocked_time.return_value = pytz.utc.localize(datetime(2021, i, i))
                user = User.objects.create(username=name, email=f"{name}@email.com")

    # def setUp(self) -> None:
    #     """Create Users & Posts"""
    #     for i, name in enumerate(["john", "mary", "paddy", "betty", "tom"], start=1):
    #         with mock.patch("django.utils.timezone.now") as mocked_time:
    #             mocked_time.return_value = pytz.utc.localize(datetime(2021, i, i))
    #             user = User.objects.create(username=name, email=f"{name}@email.com")
    #             Post.objects.create(creator=user, content=f"post-{i}", pub_date=timezone.now())

    def test_model_relation_no_information(self):
        """
        Verify error raised when saving Follow with no information
        """
        follow = Follow()
        with self.assertRaises(IntegrityError):
            follow.clean()
            follow.save()

    def test_model_relation_following_missing(self):
        """
        Verify can save Follow without specifying following
        """
        user = User.objects.all()[1]
        follow = Follow(user=user)
        follow.clean()
        follow.save()

    def test_model_relation_following(self):
        """
        Verify users added to following relation
        """
        user = User.objects.get(id=1)
        follow = Follow.objects.create(user=user)
        for user in User.objects.exclude(id=1):
            follow.following.add(user)
            self.assertIn(user, Follow.objects.get(id=1).following.all())

    def test_delete_user(self):
        """
        Verify that deleting a User from db deletes its Follow
        """
        user = User.objects.get(id=1)
        follow = Follow.objects.create(user=user)
        self.assertTrue(Follow.objects.filter(user=user).exists())
        follow.delete()
        self.assertFalse(Follow.objects.filter(user=user).exists())

    def test_delete_user_following(self):
        """
        Verify that deleting a User from db deletes removes it from following
        """
        user = User.objects.get(id=1)
        user2 = User.objects.get(id=2)
        follow = Follow.objects.create(user=user)
        follow.following.add(user2)
        self.assertIn(user2, Follow.objects.get(id=1).following.all())
        user2.delete()
        self.assertNotIn(user2, Follow.objects.get(id=1).following.all())

    def test_unique_constraint(self):
        """
        Verify that user cannot create multiple Follow lists
        """
        user = User.objects.get(id=1)
        Follow.objects.create(user=user)
        with self.assertRaises(IntegrityError):
            Follow.objects.create(user=user)

    def test_cannot_follow_oneself(self):
        """
        verify that user cannot follow themselves
        """
        user = User.objects.get(id=1)
        follow = Follow.objects.create(user=user)
        with self.assertRaises(ValidationError):
            follow.following.add(user)

    def test_object_name(self):
        """
        Verify __str__ method returns:
        'Follow #{follow.id} - {user}'s follows list'
        """
        user = User.objects.get(id=1)
        follow = Follow.objects.create(user=user)
        actual = str(follow)
        expected = f"Follow #{follow.id} - {user}'s follows list"
        self.assertEqual(actual, expected)