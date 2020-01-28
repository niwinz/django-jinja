#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import sys


INSTALL_REQUIRES = [
    "jinja2 >=2.5",
    "django >=1.11, <3.1",
]

if sys.version_info < (2, 7):
    INSTALL_REQUIRES.append("importlib")

setup(
    name = "django-jinja",
    version = "2.5.0",
    description = "Jinja2 templating language integrated in Django.",
    long_description = "",
    keywords = "django, jinja2",
    author = "Andrey Antukh",
    author_email = "auvipy@gmail.com",
    url = "https://github.com/niwinz/django-jinja",
    license = "BSD",
    packages = [
        "django_jinja",
        "django_jinja.builtins",
        "django_jinja.management",
        "django_jinja.management.commands",
        "django_jinja.contrib",
        "django_jinja.contrib._pipeline",
        "django_jinja.contrib._pipeline.templatetags",
        "django_jinja.contrib._easy_thumbnails",
        "django_jinja.contrib._easy_thumbnails.templatetags",
        "django_jinja.contrib._humanize",
        "django_jinja.contrib._humanize.templatetags",
        "django_jinja.contrib._subdomains",
        "django_jinja.contrib._subdomains.templatetags",
        "django_jinja.views",
        "django_jinja.views.generic",
    ],

    install_requires = INSTALL_REQUIRES,
    tests_require = [
        "pytz",
    ],

    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP",
    ]
)
