from .authentication import *

# -----------------------------------------------------------------------------
# Business Logic Custom Variables and Settings
# -----------------------------------------------------------------------------
from .business_logic import *
from .cache import *
from .celery import *
from .databases import *
from .drf import *
from .health_check import *
from .installed_apps import *
from .internationalization import *
from .logging import *
from .middleware import *
from .paths import *
from .storage import *
from .templates import *

APPEND_SLASH = False
ALLOWED_HOSTS = ["*"]
SITE_ID = 1
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TESTING = False
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Custom settings
APP_LABEL = "Project Tracker"
