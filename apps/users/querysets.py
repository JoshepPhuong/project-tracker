import typing

from django.db import models
from django.db.models.functions import Concat


class UserQuerySet(models.QuerySet):
    """Custom Queryset for User model."""

    def with_fullname(self) -> typing.Self:
        """Annotate fullname."""
        return self.annotate(
            fullname=Concat("first_name", models.Value(" "), "last_name"),
        )

    def with_activation_status(self) -> typing.Self:
        """Annotate activation status."""
        return self.annotate(
            activation_status=models.Case(
                models.When(
                    deactivated_at__isnull=False,
                    then=models.Value("Inactive"),
                ),
                default=models.Value("Active"),
                output_field=models.CharField(),
            ),
        )
