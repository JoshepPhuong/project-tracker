import sys

import decouple

from .common import *

DEBUG = decouple.config("DEBUG", default=False, cast=bool)

# Enable restriction to access debug tools like swagger, django debug toolbars,
# Admin page for prod environment
RESTRICT_DEBUG_ACCESS = bool(DEBUG)

ENVIRONMENT = decouple.config("ENVIRONMENT")

FRONTEND_URL = decouple.config("FRONTEND_URL", default="")

DATABASES["default"].update(
    NAME=decouple.config("RDS_DB_NAME"),
    USER=decouple.config("RDS_DB_USER"),
    PASSWORD=decouple.config("RDS_DB_PASSWORD"),
    HOST=decouple.config("RDS_DB_HOST"),
    PORT=decouple.config("RDS_DB_PORT"),
)

# Use Cloudflare R2 for media storage
AWS_STORAGE_BUCKET_NAME = decouple.config("AWS_S3_BUCKET_NAME")
AWS_S3_ACCESS_KEY_ID = decouple.config("AWS_S3_ACCESS_KEY_ID")
AWS_S3_SECRET_ACCESS_KEY = decouple.config("AWS_S3_SECRET_ACCESS_KEY")
AWS_S3_ACCOUNT_ID = decouple.config("AWS_S3_ACCOUNT_ID")
AWS_S3_ENDPOINT_URL = f"https://{AWS_S3_ACCOUNT_ID}.r2.cloudflarestorage.com"
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_CUSTOM_DOMAIN = decouple.config("R2_PUBLIC_URL")
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_UI_URL = decouple.config("EMAIL_UI_URL")
EMAIL_HOST = decouple.config("EMAIL_HOST")
EMAIL_HOST_USER = decouple.config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = decouple.config("EMAIL_HOST_PASSWORD")
EMAIL_PORT = decouple.config("EMAIL_HOST_PORT", cast=int)
EMAIL_USE_TLS = decouple.config("EMAIL_HOST_USE_TLS", cast=bool)
DEFAULT_FROM_EMAIL = (
    decouple.config("DEFAULT_FROM_EMAIL")
    or "no-reply@project-tracker-backend.com"
)

redis_host = decouple.config("REDIS_HOST")
redis_port = decouple.config("REDIS_PORT", cast=int)
redis_db = decouple.config("REDIS_DB", cast=int)
MIGRATION_DATA_FOLDER = decouple.config("MIGRATION_DATA_FOLDER", default="")

CELERY_BROKER_URL = f"redis://{redis_host}:{redis_port}/{redis_db}"
CELERY_RESULT_BACKEND = f"redis://{redis_host}:{redis_port}/{redis_db}"

# Setting needed for redis health check
REDIS_URL = f"redis://{redis_host}:{redis_port}/{redis_db}"

CACHES["default"].update(
    LOCATION=REDIS_URL,
)

SECRET_KEY = decouple.config("DJANGO_SECRET_KEY")
DOMAIN_NAME = decouple.config("DOMAIN_NAME", default="localhost")
ALLOWED_HOSTS = [DOMAIN_NAME]
CSRF_TRUSTED_ORIGINS = [f"https://{DOMAIN_NAME}"]

# disable django DEBUG if we run celery worker
if "celery" in sys.argv[0]:
    DEBUG = False

if DEBUG:
    # Dev tools settings
    from .common.dev_tools import *
