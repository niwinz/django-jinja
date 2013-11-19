Contrib modules
===============

django-jinja comes with integration with other applications in django.

At the moment, it only has one contrib app, but in future it can integrate with others.

django-pipeline
---------------

Pipeline_ is an asset packaging library for Django (official description).

.. _Pipeline: https://github.com/cyberdelia/django-pipeline

To activate this plugin add ``django_jinja.contrib._pipeline`` to your ``INSTALLED_APPS`` tuple:

.. code-block:: python

    INSTALLED_APPS += ('django_jinja.contrib._pipeline',)

Now, you can use ``compressed_css`` and ``compressed_js`` as global functions:

.. code-block:: jinja

    <!DOCTYPE html>
    <html>
        <head>
            <title>Foo</title>
            {{ compressed_css("main") }}
        </head>
        <body>
            <!-- body -->
        </body>
    </html>


easy_thumbnails
---------------

Easy Thumbnails is a thumbnail generation library for Django.

To activate this plugin add ``django_jinja.contrib._easy_thumbnails`` to your ``INSTALLED_APPS`` tuple:

.. code-block:: python

    INSTALLED_APPS += ('django_jinja.contrib._easy_thumbnails',)

Now, you can use the ``thumbnail`` global function:

.. code-block:: jinja

    <!DOCTYPE html>
    <html>
        <head>
            <title>Foo</title>
        </head>
        <body>
            <img src="{{ thumbnail(file, size=(400, 400)) }}">
        </body>
    </html>


django-subdomains
-----------------

Subdomain helpers for the Django framework, including subdomain-based URL routing.

To activate this plugin add ``django_jinja.contrib._subdomains`` to your ``INSTALLED_APPS`` tuple:

.. code-block:: python

    INSTALLED_APPS += ('django_jinja.contrib._subdomains',)

Now you can use the ``url`` global function with the subdomain parameter:

.. code-block:: jinja

    <!DOCTYPE html>
    <html>
        <head>
            <title>Foo</title>
        </head>
        <body>
            <img src="{{ url('homepage', subdomain='wildcard') }}">
        </body>
    </html>


dajax-ice
---------

Easy to use AJAX library for django.

First, follow the install instructions in
`Dajaxice Quickstart <http://django-dajaxice.readthedocs.org/en/latest/index.html#>`_.    

Then, activate this plugin by adding ``django_jinja.contrib._dajaxice`` to your ``INSTALLED_APPS`` tuple:

.. code-block:: python

    INSTALLED_APPS = (
    #...,
    #...,
    #...,
    'django_jinja',
    'django_jinja.contrib._pipeline', 
    'django_jinja.contrib._dajaxice', 
    'dajaxice',
    )
    
Now you can use the ``dajaxice_js_import`` global context function:

.. code-block:: jinja

    <!DOCTYPE html>
    <html>
        <head>
            <title>Foo</title>
            {{ dajaxice_js_import() }}            
        </head>
        <body>
            ...
        </body>
    </html>

Troubleshooting

* ImportError: No module named defaults

  * try downgrading to Django 1.5.x
  