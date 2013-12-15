Quickstart
==========

Install
-------

You can download tarball from Pypi_, extract this and install with:

.. _Pypi: http://pypi.python.org/pypi/django-jinja/

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

You can specify the default extension for jinja2 with this settings:

.. code-block:: python

    DEFAULT_JINJA2_TEMPLATE_EXTENSION = '.jinja'


With **0.13** version, **django-jinja** incorporates more flexible method for
intercept templates, using regex for matching.

Note: this method has worse perfomance that the default intercept
method (by extension):


.. code-block:: python

    # Same behavior of default intercept method
    # by extension but using regex (not recommended)
    DEFAULT_JINJA2_TEMPLATE_INTERCEPT_RE = r'.*jinja$'

    # More advanced method. Intercept all templates
    # except from django admin.
    DEFAULT_JINJA2_TEMPLATE_INTERCEPT_RE = r"^(?!admin/).*"


Optional settings
-----------------

Additionally, **django-jinja** exposes some other settings parameters for costumize your jinja2 environment:

**JINJA2_ENVIRONMENT_OPTIONS**

Low level kwargs parameters for a jinja2 ``Environment`` instance. Example usage:

.. code-block:: python

    JINJA2_ENVIRONMENT_OPTIONS = {
        'block_start_string' : '\BLOCK{',
        'block_end_string' : '}',
        'variable_start_string' : '\VAR{',
        'variable_end_string' : '}',
        'comment_start_string' : '\#{',
        'comment_end_string' : '}',
        'line_statement_prefix' : '%-',
        'line_comment_prefix' : '%#',
        'trim_blocks' : True,
        'autoescape' : False,
    }

**JINJA2_AUTOESCAPE**

Boolean value that enables or disables template autoescape. Default value is ``True``

**JINJA2_MUTE_URLRESOLVE_EXCEPTIONS**

Boolean value that mute reverse url exceptions produced by url tag. Defaul value is ``False``


Bytecode caching
----------------

**django-jinja** supports the use of Jinja2's template bytecode caching system to improve performance. It includes a default Jinja2 bytecode cache implementation that makes use of Django's built-in cache framework. This way, the template bytecode can be stored into a Django cache backend configured in your project via the CACHES_ setting. However, you can also use your own Jinja2 bytecode cache class.

.. _CACHES: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-CACHES


**JINJA2_BYTECODE_CACHE_ENABLE**

A boolean value that enables or disables bytecode caching. Defaults to ``False``.


**JINJA2_BYTECODE_CACHE_NAME**

The name of the Django cache backend to use for storing the template bytecode, as defined in your CACHES setting. Defaults to ``'default'``.


**JINJA2_BYTECODE_CACHE_BACKEND**

A dotted path to a Jinja2 bytecode cache class. See the Jinja2 docs_ for reference if you want to implement your own cache class. Defaults to the backend built in to **django-jinja** (``'django_jinja.cache.BytecodeCache'``).

.. _docs: http://jinja.pocoo.org/docs/api/#bytecode-cache
