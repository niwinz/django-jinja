from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testmodel',
            name='date',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
