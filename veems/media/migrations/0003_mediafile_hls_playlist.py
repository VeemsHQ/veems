# Generated by Django 3.1.4 on 2020-12-17 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_mediafile_metadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediafile',
            name='hls_playlist',
            field=models.TextField(null=True),
        ),
    ]