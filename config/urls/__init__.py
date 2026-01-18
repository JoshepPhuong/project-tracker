from django.contrib import admin
from django.urls import include, path

from libs.health_checks import liveness_check

from apps.core.views import IndexView
from apps.users.urls import urlpatterns as users_urlpatterns

from .api_versions import urlpatterns as api_urlpatterns
from .debug import urlpatterns as debug_urlpatterns

urlpatterns = [
    path("mission-control-center/", admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    # Django Health Check url
    # See more details: https://pypi.org/project/django-health-check/
    # Custom checks at lib/health_checks
    path(
        "healthz/",
        include(
            "health_check.urls",
            namespace="healthz",
        ),
        name="healthz",
    ),
    path(
        "livez/",
        liveness_check.liveness_check,
        name="livez",
    ),
    path(
        "readyz/",
        liveness_check.liveness_check,
        name="readyz",
    ),
]

urlpatterns += api_urlpatterns
urlpatterns += debug_urlpatterns
urlpatterns += users_urlpatterns
