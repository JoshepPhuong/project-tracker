from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class ProjectStatuses(TextChoices):
    """Project statuses choices."""

    PLANNED = "planned", _("Planned")
    IN_PROGRESS = "in_progress", _("In Progress")
    COMPLETED = "completed", _("Completed")
    CANCELED = "canceled", _("Canceled")


class TaskStatuses(TextChoices):
    """Task statuses choices."""

    TODO = "todo", _("To Do")
    IN_PROGRESS = "in_progress", _("In Progress")
    DONE = "done", _("Done")
