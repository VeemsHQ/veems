# Generated by Django 3.1.6 on 2021-02-20 13:54

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0010_upload_provider_upload_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='presigned_upload_urls',
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.URLField(max_length=500),
                null=True,
                size=None,
            ),
        ),
    ]
