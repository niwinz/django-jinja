Contrib modules
===============

django-jinja comes with integration with other applications in django.

At the momento, has only one contrib app, but in near future can integrate with others.

django-pipeline
---------------

Pipeline_ is an asset packaging library for Django (official description).

.. _Pipeline: https://github.com/cyberdelia/django-pipeline

For activate this plugin add ``django_jinja.contrib.pipeline`` on your's installed apps tuple:

.. code-block:: python

    INSTALLED_APPS += ('django_jinja.contrib.pipeline',)

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
