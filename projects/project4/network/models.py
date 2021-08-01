from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    pass


class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    content = models.CharField(max_length=160)
    pub_date = models.DateTimeField('date posted', default=timezone.now)

    class Meta:
        ordering = ["-pub_date"]

    @property
    def likes_count(self):
        return self.likes.filter(like_unlike=True).count()

    @property
    def unlikes_count(self):
        return self.likes.filter(like_unlike=False).count()

    def __str__(self):
        return f"{self.id} - By {self.creator}"


BOOL_CHOICES = ((True, "like"), (False, "unlike"))


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like_unlike = models.BooleanField(choices=BOOL_CHOICES, null=False)

    @property
    def like_unlike_wording(self):
        return "like" if self.like_unlike else "unlike"

    def clean(self):
        """Prevent User from liking/unliking their own post"""
        if self.user == self.post.creator:
            raise ValidationError(_(f"User cannot {self.like_unlike_wording} their own post"))

    class Meta:
        constraints = [
            # Prevent a user from liking/unliking the same post twice
            models.UniqueConstraint(fields=['user', 'post'], name="unique like"),
        ]

    # def post_creator(self):
    #     return self.post.creator

    def __str__(self):
        return f"Post #{self.post.id} - {self.user} {self.like_unlike_wording}s this"


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name="following")

    class Meta:
        constraints = [
            # Prevent a user from creating multiple Follow lists
            models.UniqueConstraint(fields=['user'], name="unique follow list"),
        ]

    def __str__(self):
        return f"Follow #{self.id} - {self.user}'s follows list"
