from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class UserRoles(TextChoices):
    """User roles choices."""

    ADMIN = "admin", _("Admin")
    CLIENT = "client", _("Client")
