from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Repository(BaseModel):
    """Repository model."""

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        unique=True,
    )
    url = models.URLField(
        verbose_name=_("URL"),
        unique=True,
    )
    project = models.ForeignKey(
        to="projects.Project",
        verbose_name=_("Project"),
        on_delete=models.CASCADE,
        related_name="repositories",
    )

    class Meta:
        verbose_name = _("Repository")
        verbose_name_plural = _("Repositories")

    def __str__(self) -> str:
        return self.name
