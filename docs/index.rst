.. django-jinja documentation master file, created by
   sphinx-quickstart on Sun Feb 17 10:22:05 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

django-jinja
============

Release v\ |version|.

django-jinja is a :ref:`BSD Licensed`, simple and nonobstructive jinja2 integration with Django.


Introduction
------------

Jinja2 provides certain advantages over the native system of Django, for example, explicit calls to
callable from templates, has better performance and has a plugin system, etc ...

There are other projects that attempt do same thing: Djinja, Coffin, etc... Why one more?

- Unlike Djinja, **django-jinja** is not intended to replace a Django template engine, but rather, it complements the Django's template engine, giving the possibility to use both.
- Unlike Coffin, the django-jinja codebase is much smaller and more modern. This way is much more maintainable and easily understandable how the library works.


Features
--------

- Auto-load templatetags compatible with Jinja2 on same way as Django.
- Django templates can coexist with Jinja2 templates without any problems.
  It works as middleware, intercepts Jinja templates by file path pattern.
- Django template filters and tags can mostly be used in Jinja2 templates.
- I18n subsystem adapted for Jinja2 (makemessages now collects messages from Jinja templates)
- Compatible with python2 and python3 using same codebase.
- Supported django versions: 1.4, 1.5, 1.6+

.. versionadded:: 0.13
    Regex template intercept (it gives a lot of flexibility with slighty
    performance decrease over a default intercept method).

.. versionadded:: 0.21
    Optional support for bytecode caching that uses Django's built-in cache framework by default.


User guide
----------

.. toctree::
   :maxdepth: 1

   quickstart.rst
   differences.rst
   contrib.rst
