# Generated by Django 3.1.6 on 2021-02-17 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0008_auto_20210214_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='filename',
            field=models.TextField(default=None, max_length=500),
            preserve_default=False,
        ),
    ]
