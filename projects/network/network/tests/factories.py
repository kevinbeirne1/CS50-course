from datetime import datetime

import factory
import pytz

from .. import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User
        django_get_or_create = ('username',)

    username = factory.Faker('name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'P@ssword!')


class PostFactory(factory.django.DjangoModelFactory):

    content = factory.Sequence(lambda n: f"Post #{n}")
    creator = factory.SubFactory(UserFactory)
    pub_date = factory.Sequence(lambda n: pytz.utc.localize(datetime(2021, 1, n + 1)))

    class Meta:
        model = models.Post
