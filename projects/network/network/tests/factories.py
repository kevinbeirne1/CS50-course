from datetime import datetime

import factory
import pytz

from .. import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username = 'harry'
    email = 'hpotter@email.com'
    password = factory.PostGenerationMethodCall('set_password', 'P@ssword!')


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Post

    content = "A new post"
    creator = factory.SubFactory(UserFactory)
    pub_date = pytz.utc.localize(datetime(2021, 1, 1))
