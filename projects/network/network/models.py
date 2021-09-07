from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Post(models.Model):
    content = models.CharField(max_length=160)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    pub_date = models.DateTimeField(default=timezone.now)

