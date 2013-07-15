Differences
===========

In django, creating new tags is simpler than in Jinja2. You should remember that
in jinja tags are really extensions and have a different purpose than the django template tags.

Thus for many things that the django template system uses tags, django-jinja will provide
functions with the same functionality.


Reverse urls on templates
-------------------------

In django you are accustomed to using the url tag:

.. code-block:: jinja

    {% url 'ns:name' pk=obj.pk %}

With jinja, you can use **reverse** filter or **url** global function. For example:

.. code-block:: jinja

    {{ 'ns:name'|reverse(pk=obj.pk) }}
    {{ url('ns:name', pk=obj.pk) }}


Static files tag
----------------

On modern django apps we are accustomed to seeing a **static** template tag:

.. code-block:: jinja

    {% load static from staticfiles %}
    {% static "js/lib/foo.js" %}
    {% static "js/lib/foo.js" as staticurl %}

Jinja exposes a **static** global function or a **static** filter which does the same thing:

.. code-block:: jinja

    {{ "js/lib/foo.js"|static }}
    {{ static("js/lib/foo.js" ) }}
    {% set staticurl = static("js/lib/foo.js" ) %}


I18N and Django gettext
-----------------------

**django-jinja** has a built-in extension to the ``makemessages`` command, that correctly collects
messages from jinja templates.

Here is an example:

.. code-block:: console

    python manage.py makemessages -a -e py,jinja,html

.. code-block:: jinja

    {{ _('i18n data') }}
    {% trans %}
        i18n data
    {% endtrans %}


Register global functions
-------------------------

You can register your global functions as you are registering template tags or filters in django.

Simple example:

.. code-block:: python

    # <someapp>/templatetags/<anyfile>.py
    from django_jinja import library

    lib = library.Library()

    @lib.global_function
    def myupper(name):
        return name.upper()

Functions, filters, or tests are registered globally on jinja automatically, without an explicit
load templatetag.


Render 4xx/500 pages with jinja
-------------------------------

Because django-jinja works as middleware that intercepts template rendering, standard django
sepecial handlers (views) do not use jinja to render 404, 403 or 500 pages. To fix this, you can
define your own views or use django-jinja's predefined ones.

Example:

.. code-block:: python

    # Your main urls.py
    from django_jinja import views

    handler403 = views.PermissionDenied.as_view()
    handler404 = views.PageNotFound.as_view()
    handler500 = views.ServerError.as_view()
