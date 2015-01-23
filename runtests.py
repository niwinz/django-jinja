# -*- coding: utf-8 -*-

import sys, os
import django

from django.conf import settings
from django.core.management import call_command

TEST_TEMPLATE_DIR = "templates"
RUNTESTS_DIR = os.path.dirname(__file__)
sys.path.insert(0, "testing")


test_settings = {
    "DATABASES":{
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
        }
    },
    "INSTALLED_APPS": [
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.staticfiles",
        "django.contrib.messages",
        "django_jinja",
        "testapp",
        "pipeline",
        "django_jinja.contrib._pipeline",
    ],
    "INTERNAL_IPS": ("127.0.0.1",),
    "ROOT_URLCONF":"testapp.urls",
    "STATIC_URL":"/static/",
    "STATIC_ROOT": os.path.join(RUNTESTS_DIR, "static"),
    "TEMPLATE_DIRS":(
        os.path.join(RUNTESTS_DIR, TEST_TEMPLATE_DIR),
    ),
    "USE_I18N": True,
    "USE_TZ": True,
    "LANGUAGE_CODE":"en",
    "MIDDLEWARE_CLASSES": (
        "django.middleware.common.CommonMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ),
    "MANAGERS": ("niwi@niwi.be",),
    "TEMPLATE_LOADERS": [
        "django_jinja.loaders.AppLoader",
        "django_jinja.loaders.FileSystemLoader",
    ],
    "PIPELINE_CSS": {
        "test": {
            "source_filenames": ["style.css"],
            "output_filename": "style.2.css",
            "extra_context": {"media": "all"},
        },
        "test2": {
            "source_filenames": ["style.css"],
            "output_filename": "style.2.css",
        }
    },
    "PIPELINE_JS": {
        "test": {
            "source_filenames": ["script.js"],
            "output_filename": "script.2.js",
        }
    },
    "JINJA2_CONSTANTS": {"foo": "bar"},
    "JINJA2_AUTOESCAPE": True,
    "JINJA2_MUTE_URLRESOLVE_EXCEPTIONS": True,
    "TEMPLATES": [
        {"BACKEND": "django_jinja.backend.Jinja2",
         "NAME": "jinja2",
         "APP_DIRS": True,
         "OPTIONS": {
             "context_processors": [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
             ]
         }}
     ],
}


if django.VERSION[:2] >= (1, 6):
    test_settings["TEST_RUNNER"] = "django.test.runner.DiscoverRunner"


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    if not settings.configured:
        settings.configure(**test_settings)

    args = sys.argv
    args.insert(1, "test")
    args.insert(2, "testapp")

    execute_from_command_line(args)
