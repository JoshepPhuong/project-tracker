# Custom model for Auth
AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = (
    "rules.permissions.ObjectPermissionBackend",
    "django.contrib.auth.backends.ModelBackend",
    "apps.users.auth_backends.EmailBackend",
)

LOGIN_REDIRECT_URL = "/user/profile/"
LOGIN_URL = "/user/login/"
