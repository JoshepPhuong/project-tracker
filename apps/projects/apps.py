from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProjectsAppConfig(AppConfig):
    """Default configuration for Projects app."""

    name = "apps.projects"
    verbose_name = _("Projects")
