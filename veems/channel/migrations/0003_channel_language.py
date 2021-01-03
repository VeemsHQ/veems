# Generated by Django 3.1.4 on 2020-12-28 19:29

from django.db import migrations, models
import veems.common.validators


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0002_auto_20201228_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='language',
            field=models.CharField(
                default=None,
                max_length=2,
                validators=[veems.common.validators.validate_language],
            ),
            preserve_default=False,
        ),
    ]
