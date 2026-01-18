from __future__ import annotations

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

import citext

from apps.core.models import BaseModel

from .. import constants
from .. import managers


class User(
    BaseModel,
    AbstractBaseUser,
    PermissionsMixin,
):
    """Custom user model."""

    first_name = models.CharField(
        verbose_name=_("First name"),
        max_length=255,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name=_("Last name"),
        max_length=255,
        null=True,
        blank=True,
    )
    username = models.CharField(
        verbose_name=_("Username"),
        max_length=255,
        unique=True,
    )
    email = citext.CIEmailField(
        verbose_name=_("Email address"),
        unique=True,
    )
    is_staff = models.BooleanField(
        verbose_name=_("Staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site.",
        ),
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active.",
        ),
    )
    role = models.CharField(
        verbose_name=_("Role"),
        max_length=50,
        choices=constants.UserRoles.choices,
        default=constants.UserRoles.CLIENT,
    )
    client = models.ForeignKey(
        to="users.Client",
        verbose_name=_("Client"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    avatar = models.ImageField(
        verbose_name=_("Avatar"),
        blank=True,
        null=True,
        upload_to=settings.DEFAULT_MEDIA_PATH,
        max_length=512,
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = managers.UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f"{self.username} ({self.email})"

    @property
    def full_name(self) -> str:
        """Return user's full name.

        Returns:
            str: first name + last name

        """
        return f"{self.first_name} {self.last_name}"
