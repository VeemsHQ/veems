# Generated by Django 3.1.6 on 2021-02-20 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0009_video_filename'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='provider_upload_id',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]