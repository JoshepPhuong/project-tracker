from .health_check import HEALTH_CHECKS_APPS

# Application definition
INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django.contrib.gis",
)

DRF_PACKAGES = (
    "rest_framework",
    "django_filters",
    "knox",
    "drf_spectacular",
    "drf_standardized_errors",
)

THIRD_PARTY = (
    "storages",
    "django_celery_beat",
    "django_extensions",
    "rules",
    "citext",
    "crispy_forms",
    "crispy_bootstrap4",
)

LOCAL_APPS = (
    "apps.core",
    "apps.auth",
    "apps.users",
    "apps.projects",
)

INSTALLED_APPS += DRF_PACKAGES + THIRD_PARTY + HEALTH_CHECKS_APPS + LOCAL_APPS
