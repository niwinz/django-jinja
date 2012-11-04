Jinja2 templating language integrated in Django.
================================================

Django application for integrating jinja2 template system.

Jinja2 provides certain advantages over the native system of django, for example, explicit calls to
callable from templates, has more performance and has a plugin system, etc ...

There is another project like this: Djinja. Unlike him, ``django-jinja`` is not intended to replace the
django templates, but it complements the django templates, giving the possibility to use both. Thus no
need to adapt applications to use django jinja2 only use it where you need it.

Another advantage of "django-jinja" is that you can still use django as before, regardless of specific helper or specific shortcuts.

Features:
---------

* Auto load templatetags compatible with jinja2
* Can combine django templates with jinja2 templates.
* A lot of django template filters ported for work with jinja2


How to install?
---------------

You can download tarball from <http://pypi.python.org/pypi/django-jinja/>, extract this and install with:

.. code-block:: shell

    tar xvf django-jinja-x.y.tar.gz
    cd django-jinja
    python setup.py install

Other alternative is install with ``pip``:

.. code-block:: shell

    pip install django-jinja


How to use this on your django project?
---------------------------------------

As a first and only step, you have to replace django template_loaders by django-jinja2 loaders:

.. code-block:: python

    # settings.py
    TEMPLATE_LOADERS = (
        'django_jinja.loaders.AppLoader',
        'django_jinja.loaders.FileSystemLoader',
    )

    INSTALLED_APPS += ('django_jinja',)

Now you can place templates (".jinja" extension) as you would with normal django templates.

You can specify the default extension for jinja2 by the parameter ``DEFAULT_JINJA2_TEMPLATE_EXTENSION`` in ``settings.py``:

.. code-block:: python

    # settings.py
    DEFAULT_JINJA2_TEMPLATE_EXTENSION = '.jinja'

You can also assign different options to the Environment by ``JINJA2_ENVIRONMENT_OPTIONS`` parameter.
To see more details, please see the sample application.

Additionally you can specify whether or not to activate Autoescape extension with
``JINJA2_AUTOESCAPE`` boolean parameter. By default is desactivated.


Django filters and functions:
-----------------------------

Url reverse:
^^^^^^^^^^^^

Useful for reverse urls on templates. Currently have two alternatives: filter or function.

Usage examples:

.. code-block:: jinja

    {{ 'ns:urlaname'|reverse(arg1=val1) }}
    {{ url('ns:urlaname', arg1=val1) }}


Almost all of django templatefilters are available in "django-jinja", and if you find one at fault, patches are welcome.


I18N and Django gettext
-----------------------

``django-jinja`` incorporates an extension to makemessages command, so you can deal with differences of translations jinja tags.

This is an example of use:

.. code-block:: python

    python ../manage.py makemessages  -a -e py,jinja,html

.. .. toctree::
    :maxdepth: 2

..  Indices and tables
    ==================
    * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`

