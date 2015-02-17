import os, sys

sys.path.insert(0, "..")

BASE_DIR = os.path.dirname(__file__)
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    }
}

MIDDLEWARE_CLASSES = [
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

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, "static"),
# )


# STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
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

TEMPLATE_LOADERS = [
   "django_jinja.loaders.AppLoader",
   "django_jinja.loaders.FileSystemLoader"
]

# TEMPLATES = [
#    {"BACKEND": "django_jinja.backend.Jinja2",
#     "NAME": "jinja2",
#     "APP_DIRS": True,
#     "OPTIONS": {
#         "context_processors": [
#            "django.contrib.auth.context_processors.auth",
#            "django.template.context_processors.debug",
#            "django.template.context_processors.i18n",
#            "django.template.context_processors.media",
#            "django.template.context_processors.static",
#            "django.template.context_processors.tz",
#            "django.contrib.messages.context_processors.messages",
#         ]
#     }}
# ]

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

JINJA2_CONSTANTS = {"foo": "bar"}
JINJA2_AUTOESCAPE = True
JINJA2_MUTE_URLRESOLVE_EXCEPTIONS = True
JINJA2_TEMPLATE_EXTENSION = '.jinja'

import django
if django.VERSION[:2] >= (1, 6):
    TEST_RUNNER = "django.test.runner.DiscoverRunner"
