# Generated by Django 3.1.4 on 2020-12-18 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0006_auto_20201217_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediafile',
            name='codecs_string',
            field=models.CharField(max_length=100, null=True),
        ),
    ]