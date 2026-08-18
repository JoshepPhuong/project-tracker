from django.contrib.auth.models import UserManager as DjangoUserManager

from . import constants, querysets


class UserManager(DjangoUserManager.from_queryset(querysets.UserQuerySet)):
    """Adjusted user manager that works with both `username` and email."""

    def _create_user(
        self,
        username: str,
        email: str,
        password: str | None,
        **extra_fields,
    ):
        """Create and save a user with the given email and password."""
        if not (username and email):
            raise ValueError("The given username and email must be set")
        return super()._create_user(username, email, password, **extra_fields)

    def create_superuser(
        self,
        username: str,
        email: str | None = None,
        password: str | None = None,
        **extra_fields,
    ):
        """Create superuser instance (used by `createsuperuser` cmd)."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", constants.UserRoles.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)
