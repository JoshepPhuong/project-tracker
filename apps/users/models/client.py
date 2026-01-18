from django.db import models
from django.utils.translation import gettext_lazy as _

import citext

from apps.core.models import BaseModel


class Client(BaseModel):
    """Client model."""

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
    )
    email = citext.CIEmailField(
        verbose_name=_("Email address"),
        unique=True,
    )
    phone_number = models.CharField(
        verbose_name=_("Phone number"),
        max_length=20,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")

    def __str__(self) -> str:
        return self.name
