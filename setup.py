#!/usr/bin/env python3

from setuptools import setup

setup(
    name = "django-jinja",
    version = "2.7.0",
    description = "Jinja2 templating language integrated in Django.",
    long_description = open("README.rst").read(),
    long_description_content_type='text/x-rst',
    keywords = "django, jinja2",
    author = "Andrey Antukh",
    author_email = "niwi@niwi.be",
    maintainer = "Asif Saif Uddin",
    maintainer_email = "auvipy@gmail.com",
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
    python_requires = ">=3.5",
    install_requires = [
        "jinja2>=2.10",
        "django>=2.2",
    ],
    tests_require = [
        "pytz",
    ],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP",
    ]
)
