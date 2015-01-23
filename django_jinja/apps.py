import django

from django.apps import AppConfig
from django_jinja import base


class DjangoJinjaAppConfig(AppConfig):
    name = "django_jinja"
    verbose_name = "Django Jinja"

    def ready(self):
        if django.VERSION[:2] <= (1, 7):
            base.setup_django_lte_17()
        else:
            base.setup_django_gte_18()
