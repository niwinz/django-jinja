import os, sys
sys.path.insert(0, "..")

BASE_DIR = os.path.dirname(__file__)
DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "foobar.db"
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

MIDDLEWARE_CLASSES = [
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "testapp.urls"

USE_I18N =  True
USE_TZ = True
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en"
ADMIN_MEDIA_PREFIX = "/static/admin/"
INTERNAL_IPS = ("127.0.0.1",)

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

# TEMPLATE_DIRS = ()

SECRET_KEY = "di!n($kqa3)nd%ikad#kcjpkd^uw*h%*kj=*pm7$vbo6ir7h=l"
INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "django_jinja",
    "testapp",
)

from django_jinja.builtins import DEFAULT_EXTENSIONS
JINJA2_MUTE_URLRESOLVE_EXCEPTIONS = True

TEMPLATES = [
    {
        "BACKEND": "django_jinja.jinja2.Jinja2",
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": True,
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
            "constants": {
                "foo": "bar",
            },
            "policies": {
                "ext.i18n.trimmed": True,
            },
            # "trim_blocks": True,
            # "lstrip_blocks": True,
            "extensions": DEFAULT_EXTENSIONS + [
                "django_jinja.builtins.extensions.DjangoExtraFiltersExtension",
            ]
        }
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True
    }
]

TEST_RUNNER = "django.test.runner.DiscoverRunner"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        }
    },

    "formatters": {
        "simple": {
            "format": "%(asctime)s: %(message)s",
        }
    },

    "handlers": {
        "console":{
            "level":"DEBUG",
            "class":"logging.StreamHandler",
            "formatter": "simple"
        },

    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
        "arandomtable.custom": {
            "handlers": ["console"],
            "level": "DEBUG",
        },

    }
}
