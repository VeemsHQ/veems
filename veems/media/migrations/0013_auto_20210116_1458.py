# Generated by Django 3.1.4 on 2021-01-16 14:58

from django.db import migrations, models
import veems.media.models
import veems.media.storage_backends


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0012_auto_20210102_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videorenditionsegment',
            name='file',
            field=models.FileField(
                storage=veems.media.storage_backends.MediaStoragePublic,
                upload_to=(
                    veems.media.models._video_rendition_segment_upload_to
                ),
            ),
        ),
    ]