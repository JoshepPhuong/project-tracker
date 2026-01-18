from .paths import BASE_DIR

# Django Storages
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

AWS_S3_SECURE_URLS = False
AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = "public-read"
AWS_S3_FILE_OVERWRITE = False
# Set virtual-hosted-style for S3.
# We need apply this style for local S3 storage because path-style URLs will be
# discontinued in the future, and we want to make consistent URLs for uploading
# and downloading files.
# https://docs.aws.amazon.com/AmazonS3/latest/userguide/VirtualHosting.html
AWS_S3_ADDRESSING_STYLE = "virtual"

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)
