from django.core.exceptions import ValidationError


def following_changed(sender, action, instance, *args, **kwargs):
    """Raise an error if admin tries to assign User to the Users follow list"""

    # m2mchanged.connect specified in apps.py

    following = instance.following.all()
    creator = instance.user

    if creator in following:
        raise ValidationError ("can't like own post")
