Differences
===========

In django, create new tags is relatively simpler than in jinja2. Must be understood that
in jinja tags really are extensions and have other purpose than the django template tags.

Then, for many things that the django template system uses tags, django-jinja will provide
functions with the same functionality.


Reverse urls on templates
-------------------------

In django are accustomed to use the url tag:

.. code-block:: jinja

    {% url 'ns:name' pk=obj.pk %}

With jinja, you can use **reverse** filter or **url** global function. See example:

.. code-block:: jinja

    {{ 'ns:name'|reverse(pk=obj.pk) }}
    {{ url('ns:name', pk=obj.pk) }}


Static files tag
----------------

On modern django apps, we accustomed view a **static** template tag:

.. code-block:: jinja

    {% load static from staticfiles %}
    {% static "js/lib/foo.js" %}
    {% static "js/lib/foo.js" as staticurl %}

With jinja exposes **static** global function what doing same think:

.. code-block:: jinja

    {{ static("js/lib/foo.js" ) }}
    {% set staticurl = static("js/lib/foo.js" ) %}


I18N and Django gettext
-----------------------

**django-jinja** has builtin extension to makemessages commando, that collect correctly
messages from jinja templates.

Here is an example:

.. code-block:: console

    python manage.py makemessages -a -e py,jinja,html

