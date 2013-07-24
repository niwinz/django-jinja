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
