from django.contrib import admin

from apps.core.admin import BaseAdmin
from apps.projects.models import Project

from .. import models


class ProjectInline(admin.TabularInline):
    """Inline UI for Project model on Client admin."""

    model = Project
    extra = 0
    readonly_fields = (
        "created",
        "modified",
    )
    fields = (
        "name",
        "description",
        "status",
        "created",
        "modified",
    )
    show_change_link = True


@admin.register(models.Client)
class ClientAdmin(BaseAdmin):
    """UI for Client model."""

    ordering = ("-id",)
    list_display = (
        "id",
        "name",
        "email",
        "created",
        "modified",
    )
    list_display_links = ("name",)
    search_fields = (
        "name",
        "email",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "email",
                    "phone_number",
                ),
            },
        ),
    )
    inlines = (ProjectInline,)
