from django.apps import AppConfig
from django.db.models.signals import m2m_changed
from django.utils.translation import ugettext_lazy as _
from .signals import following_changed


class NetworkConfig(AppConfig):
    name = 'network'

    def ready(self):
        follow = self.get_model("Follow")
        m2m_changed.connect(
            following_changed,
            sender=follow.following.through,
            dispatch_uid="check_following"
        )
