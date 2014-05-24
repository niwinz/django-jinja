import django

if django.get_version() < '1.7':
    from django_jinja import base
    base.initialize_environment()
