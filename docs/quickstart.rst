Quickstart
==========

Install
-------

You can download tarball from Pypi_, extract this and install with:

.. _Pypy: http://pypi.python.org/pypi/django-jinja/

.. code-block:: console

    tar xvf django-jinja-x.y.tar.gz
    cd django-jinja
    python setup.py install


Other (recomended) alternative is install with **pip**:

.. code-block:: console

    pip install django-jinja


Configure
---------

The first step is replace django **TEMPLATE_LOADERS** with a django-jinja adapted loaders,
and put ``django_jinja`` on **INSTALLED_APPS** tuple.

.. code-block:: python

    TEMPLATE_LOADERS = (
        'django_jinja.loaders.AppLoader',
        'django_jinja.loaders.FileSystemLoader',
    )

    INSTALLED_APPS += ('django_jinja',)

django-jinja template loaders inherit's from a django template loaders and add some condition for
render jinja templates.

This condition is very simple. Basically it depends on the file extension, files with ``.html`` extension
are rendered with django template engine and files with ``.jinja`` extension are rendered with jinja2 template engine.

Also, you can specify the default extension for jinja2 with this settings:

.. code-block:: python

    DEFAULT_JINJA2_TEMPLATE_EXTENSION = '.jinja'


Optional settings
-----------------

Additionally, **django-jinja** exposes some other settings parameters for costumize your jinja2 environment:

**JINJA2_ENVIRONMENT_OPTIONS**

Low level kwargs parameters for a jinja2 ``Environment`` instance.

**JINJA2_AUTOESCAPE**

Boolean value that enables or disables template autoescape.
