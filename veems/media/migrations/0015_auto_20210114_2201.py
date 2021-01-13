# Generated by Django 3.1.4 on 2021-01-14 22:01

from django.db import migrations, models
import veems.media.models
import veems.media.storage_backends


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0014_auto_20210114_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videorendition',
            name='playlist_file',
            field=models.FileField(
                storage=veems.media.storage_backends.MediaStorage,
                upload_to=(
                    veems.media.models._video_rendition_playlist_file_upload_to
                ),
            ),
        ),
    ]
