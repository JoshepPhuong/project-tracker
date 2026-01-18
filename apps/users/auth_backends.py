from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class EmailBackend(ModelBackend):
    """Authentication backend for email login."""

    def authenticate(self, request, username=None, password=None):
        """Check and return user which login with email."""
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            # Not need to re-run set_password() again
            # as it ran once in first backend checking.
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
