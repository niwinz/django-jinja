Jinja2 templating language integrated in Django.
================================================

Django application for integrating jinja2 template system.

Jinja2 provides certain advantages over the native system of django, for example, explicit calls to 
callable from templates, has more performance and has a plugin system, etc ...

There is another project like this: Djinja. Unlike him, django-jinja2 is not intended to replace the 
django templates, but it complements the django templates, giving the possibility to use both. Thus no 
need to adapt applications to use django jinja2 only use it where you need it.

Features:
---------

* Auto load templatetags compatible with jinja2
* Can combine django templates with jinja2 templates.

Under development:
------------------

* gettext/i18n scripts for jinja2 templates.
* more integration with django.
* convert some django filters for use with jinja2
* integration with django-superview

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


Djangon integration filters and functions:
------------------------------------------

Url reverse:
^^^^^^^^^^^^

Useful for reverse urls on templates. Currently have two alternatives: filter or function.

Usage examples:

.. code-block:: jinja

    {{ 'ns:urlaname'|reverse(arg1=val1) }}

    {{ url('ns:urlaname', arg1=val1) }}




.. .. toctree::
   :maxdepth: 2


..  Indices and tables
    ==================
    * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`

