#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = 'django-jinja',
    version = ":versiontools:django_jinja:",
    description = "Jinja2 templating language integrated in Django.",
    long_description = "",
    keywords = 'django, jinja2',
    author = 'Andrei Antoukh',
    author_email = 'niwi@niwi.be',
    url = 'https://github.com/niwibe/django-jinja',
    license = 'BSD',
    include_package_data = True,
    packages = find_packages(),
    install_requires=[
        'distribute',
        'jinja2',
    ],
    setup_requires = [
        'versiontools >= 1.8',
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
