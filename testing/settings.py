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

#STATICFILES_STORAGE = "pipeline.storage.PipelineStorage"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None
PIPELINE_ENABLE = False

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "pipeline.finders.PipelineFinder",
    "pipeline.finders.CachedFileFinder",
)

# TEMPLATE_DIRS = ()

SECRET_KEY = "di!n($kqa3)nd%ikad#kcjpkd^uw*h%*kj=*pm7$vbo6ir7h=l"
INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "pipeline",
    "django_jinja",
    "django_jinja.contrib._pipeline",
    "testapp",
)

from django_jinja.builtins import DEFAULT_EXTENSIONS
JINJA2_MUTE_URLRESOLVE_EXCEPTIONS = True

TEMPLATES = [
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        "NAME": "jinja2",
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

PIPELINE_CSS = {
   "test": {
       "source_filenames": ["style.css"],
       "output_filename": "style.2.css",
       "extra_context": {"media": "all"},
   },
   "test2": {
       "source_filenames": ["style.css"],
       "output_filename": "style.2.css",
   }
}


PIPELINE_JS = {
   "test": {
       "source_filenames": ["script.js"],
       "output_filename": "script.2.js",
   }
}

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
