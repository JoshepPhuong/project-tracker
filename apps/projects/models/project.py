from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel

from .. import constants


class Project(BaseModel):
    """Project model."""

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        null=True,
    )
    client = models.ForeignKey(
        to="users.Client",
        verbose_name=_("Client"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
    )
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=50,
        choices=constants.ProjectStatuses.choices,
        default=constants.ProjectStatuses.PLANNED,
    )

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self) -> str:
        return self.name


class Task(BaseModel):
    """Task model."""

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        null=True,
    )
    due_date = models.DateField(
        verbose_name=_("Due date"),
        blank=True,
        null=True,
    )
    project = models.ForeignKey(
        to="projects.Project",
        verbose_name=_("Project"),
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=50,
        choices=constants.TaskStatuses.choices,
        default=constants.TaskStatuses.TODO,
    )

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def __str__(self) -> str:
        return self.title
