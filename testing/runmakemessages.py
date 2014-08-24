# -*- coding: utf-8 -*-

import sys, os
sys.path.insert(0, "..")
sys.path.insert(0, "/home/niwi/django/")

import django

from django.conf import settings
from django.core.management import call_command

TEST_TEMPLATE_DIR = 'templates'
RUNTESTS_DIR = os.path.dirname(__file__)

# from runtests import test_settings


test_settings = {
    'DATABASES':{
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    'INSTALLED_APPS': [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.staticfiles',
        'django.contrib.messages',
        'django_jinja',
        'django_jinja_test',
        'pipeline',
        'django_jinja.contrib._pipeline',
    ],
    'INTERNAL_IPS': ('127.0.0.1',),
    'ROOT_URLCONF':'django_jinja_test.urls',
    'STATIC_URL':'/static/',
    'STATIC_ROOT': os.path.join(RUNTESTS_DIR, 'static'),
    'TEMPLATE_DIRS':(
        os.path.join(RUNTESTS_DIR, TEST_TEMPLATE_DIR),
    ),
    'USE_I18N': True,
    'USE_TZ': True,
    'LANGUAGE_CODE':'en',
    'MIDDLEWARE_CLASSES': (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ),
    'MANAGERS': ("niwi@niwi.be",),
    'TEMPLATE_LOADERS': [
        'django_jinja.loaders.AppLoader',
        'django_jinja.loaders.FileSystemLoader',
    ],
    'LANGUAGES': {"en": "English"},
    'PIPELINE_CSS': {
        'test': {
            'source_filenames': ["style.css"],
            'output_filename': "style.2.css",
        }
    },
    'PIPELINE_JS': {
        'test': {
            'source_filenames': ['script.js'],
            'output_filename': 'script.2.js',
        }
    },
    'JINJA2_CONSTANTS': {"foo": "bar"},
    'JINJA2_MUTE_URLRESOLVE_EXCEPTIONS': True,
}

if django.VERSION[:2] >= (1, 6):
    test_settings["TEST_RUNNER"] = "django.test.runner.DiscoverRunner"


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    if not settings.configured:
        settings.configure(**test_settings)

    args = sys.argv
    args.insert(1, "makemessages")
    args.insert(2, "-l")
    args.insert(3, "en")
    args.insert(4, "-e")
    args.insert(5, "jinja,html")

    execute_from_command_line(args)
