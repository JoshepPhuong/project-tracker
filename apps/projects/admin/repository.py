from django.contrib import admin

from apps.core.admin import BaseAdmin

from .. import models


@admin.register(models.Repository)
class RepositoryAdmin(BaseAdmin):
    """UI for Repository model."""

    ordering = ("-id",)
    list_display = (
        "id",
        "name",
        "url",
        "project",
        "created",
        "modified",
    )
    list_display_links = ("name",)
    search_fields = (
        "name",
        "url",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "url",
                    "project",
                ),
            },
        ),
    )
