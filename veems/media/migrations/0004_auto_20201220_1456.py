# Generated by Django 3.1.4 on 2020-12-20 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0003_auto_20201220_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='presigned_upload_url',
            field=models.URLField(max_length=1000),
        ),
    ]