from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):

    following = models.ManyToManyField('self', related_name='followers', symmetrical=False)

    @property
    def following_count(self):
        return self.following.count()

    @property
    def followers_count(self):
        return User.objects.filter(following=self).count()


class Post(models.Model):
    content = models.CharField(max_length=160)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    pub_date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='likes')

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def users_that_like(self):
        return self.likes.all()

    class Meta:
        ordering = ['-pub_date', ]
