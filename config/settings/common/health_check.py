# Settings for custom health checks
# django-health-check 4.x no longer uses the old app-based plugin registration
# or the deprecated SUBSETS config. The active health endpoint is mounted in
# config/urls/__init__.py and lists the checks explicitly there.
HEALTH_CHECKS_APPS = ("health_check",)
