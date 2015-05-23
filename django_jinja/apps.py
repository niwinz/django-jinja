import django

from django.apps import AppConfig
from django_jinja import base


class DjangoJinjaAppConfig(AppConfig):
    name = "django_jinja"
    verbose_name = "Django Jinja"

    def ready(self):
        base.patch_django_for_autoescape()
        base.patch_django_setup_test_environment()

        if django.VERSION[:2] == (1, 7):
            base.setup()
