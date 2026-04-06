from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from health_check.views import HealthCheckView
from redis.asyncio import Redis as RedisClient

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
        HealthCheckView.as_view(
            checks=[
                "health_check.Cache",
                "health_check.Database",
                "health_check.Mail",
                "health_check.Storage",
                (
                    "health_check.contrib.redis.Redis",
                    {
                        "client_factory": lambda: RedisClient.from_url(
                            settings.REDIS_URL,
                        ),
                    },
                ),
            ],
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
