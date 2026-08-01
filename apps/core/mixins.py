from typing import Any

from django.conf import settings
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


class AppStatsMixin:
    """Add app environment and open-api ui urls to context."""

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add environment and open-api ui urls to context data."""
        context = super().get_context_data(**kwargs)  # type: ignore
        open_api_ui_urls: dict[str, str | None] = {
            "swagger_api_ui": "open_api:swagger",
            "redoc_api_ui": "open_api:redoc",
        }
        for key, value in open_api_ui_urls.items():
            try:
                url = reverse(value)
            except NoReverseMatch:
                url = None
            open_api_ui_urls[key] = url
        context["env"] = settings.ENVIRONMENT
        context.update(open_api_ui_urls)
        return context
