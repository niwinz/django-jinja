.. django-jinja documentation master file, created by
   sphinx-quickstart on Sun Feb 17 10:22:05 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

django-jinja
============

Release v\ |version|.

django-jinja is a :ref:`BSD LIcensed`, simple and nonobstructive jinja2 integration with Django.

Introduction
------------

Jinja2 provides certain advantages over the native system of django, for example, explicit calls to
callable from templates, has more performance and has a plugin system, etc ...

There are another projects that attempt do same think: Djinja, Coffin, etc... Why one more?

- Unline djinja, **django-jinja** is not intended to replace a django template engine, but rather, it complements the django template engine, giving the possibility to use both.
- Unlike coffin, the django-jinja codebase is much smaller and more modern. This way is much more maintainable and easily understandable how the library works.

Features
--------

- Auto load templatetags compatible with jinja2 on same way as django.
- Can combine the django templates with jinja2 templates without any problems.
- Django template filters and tags mostly can be used on jinja2 templates.
- I18n subsystem adapted for jinja2 (makemessages now collects messages from jinja templates)
- Compatible with python2 and python3 with same codebase.


User guide
----------

.. toctree::
   :maxdepth: 1

   quickstart.rst
   differences.rst
   contrib.rst
