from django.db.models import Model, DateTimeField


class TestModel(Model):
    date = DateTimeField(null=True)
