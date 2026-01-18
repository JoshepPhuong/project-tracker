from django.conf import settings
from django.utils.translation import gettext_lazy as _

from libs.notifications.email import (
    DefaultEmailNotification,
    EmailNotification,
)

from apps.users.models import User


class ResetPasswordRequestEmailNotification(DefaultEmailNotification):
    """Used to send reset password email."""

    subject = _("Password Reset")
    template = "users/emails/password_reset_request.html"

    def __init__(self, user: User, **template_context) -> None:
        super().__init__(**template_context)
        self.user = user

    def get_recipient_list(self) -> list[str]:
        """Return email of the requesting user."""
        return [self.user.email]

    def get_template_context(self) -> dict:
        """Add the requesting user to template's context."""
        ctx = super().get_template_context()
        ctx.update(
            user=self.user,
            new_password_url=settings.FRONTEND_URL + settings.NEW_PASSWORD_URL,
            app_url=settings.FRONTEND_URL,
            app_label=settings.APP_LABEL,
        )
        return ctx


class NewPasswordEmailNotification(EmailNotification):
    """Send new password to user via email."""

    subject = _("New password for PhuongPham Blog")
    template = "users/emails/new_password.html"

    def __init__(self, user, **template_context):
        super().__init__(**template_context)
        self.user = user

    def get_recipient_list(self) -> list[str]:
        """Return email of the user."""
        return [self.user.email]

    def get_template_context(self) -> dict:
        """Add the user to template's context."""
        ctx = super().get_template_context()
        ctx["user"] = self.user
        return ctx
