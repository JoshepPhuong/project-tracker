from .paths import BASE_DIR

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Available languages
LANGUAGES = (
    ("en", "English"),
    ("es", "Spanish"),
    ("vi", "Vietnamese"),
)

# Path to store translations
LOCALE_PATHS = (BASE_DIR / "locale",)
