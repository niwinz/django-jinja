from django import VERSION

if VERSION < (3, 2):
    default_app_config = 'django_jinja.apps.DjangoJinjaAppConfig'
