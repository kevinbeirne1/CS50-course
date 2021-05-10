from django.contrib.auth import get_user_model


def reset_password(u, password):
    try:
        user = get_user_model().objects.get(username=u)
    except:
        return "User could not be found"
    user.set_password(password)
    user.save()
    return "Password has been changed successfully"


def get_superusers():
    return list(get_user_model().objects.filter(is_superuser=True).values_list('username', flat=True))