from django.contrib import admin

from apps.core.admin import BaseAdmin

from .. import models


class TaskInline(admin.TabularInline):
    """Inline UI for Task model."""

    model = models.Task
    extra = 0
    readonly_fields = ("created", "modified")
    fields = (
        "title",
        "status",
        "due_date",
        "created",
        "modified",
    )
    show_change_link = True


@admin.register(models.Project)
class ProjectAdmin(BaseAdmin):
    """UI for Project model."""

    ordering = ("-id",)
    list_display = (
        "id",
        "name",
        "status",
        "client",
        "created",
        "modified",
    )
    list_display_links = ("name",)
    list_filter = (
        "status",
    )
    search_fields = (
        "name",
        "description",
    )
    create_only_fields = ("status",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "description",
                    "status",
                    "client",
                ),
            },
        ),
    )
    inlines = (TaskInline,)
