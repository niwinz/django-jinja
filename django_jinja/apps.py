import django

from django.apps import AppConfig
from django_jinja import base


class DjangoJinjaAppConfig(AppConfig):
    name = "django_jinja"
    verbose_name = "Django Jinja"

    def ready(self):
        base.patch_django_for_autoescape()

        # This is because django apps is introduced
        # in django 1.7 but the support for multiple
        # engines is introduced in django 1.8. So
        # in django 1.7 we should initialize the global
        # jinja environment.
        if django.VERSION[:2] == (1, 7):
            base.setup()
