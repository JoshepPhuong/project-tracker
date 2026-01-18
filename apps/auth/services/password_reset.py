from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.users.models import User

from .. import notifications

NEW_PASSWORD_DEFAULT_LENGTH = 6


def request_reset_password(
    user: User,
) -> bool:
    """Request a user's password reset.

    This will send to user an email with a link where user can enter new
    password.

    """
    return notifications.ResetPasswordRequestEmailNotification(
        user=user,
        uid=urlsafe_base64_encode(force_bytes(user.pk)),
        token=PasswordResetTokenGenerator().make_token(user),
    ).send()


def reset_user_password(user: User) -> bool:
    """Reset user password to a new one.

    This will also send an email containing the new password to the user.

    """
    new_password = _generate_random_password()
    user.set_password(new_password)
    user.save()

    return notifications.NewPasswordEmailNotification(
        user=user,
        new_password=new_password,
    ).send()


def _generate_random_password():
    """Return a new random password."""
    return get_random_string(length=NEW_PASSWORD_DEFAULT_LENGTH)
