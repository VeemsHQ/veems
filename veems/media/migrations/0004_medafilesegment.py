# Generated by Django 3.1.4 on 2020-12-17 20:40

from django.db import migrations, models
import django.db.models.deletion
import veems.common.fields
import veems.media.models
import veems.media.storage_backends


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0003_mediafile_hls_playlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedaFileSegment',
            fields=[
                (
                    'id',
                    veems.common.fields.ShortUUIDField(
                        default=veems.common.fields._default,
                        editable=False,
                        max_length=12,
                        primary_key=True,
                        serialize=False
                    )
                ),
                (
                    'created_on',
                    models.DateTimeField(auto_now_add=True, db_index=True)
                ),
                (
                    'modified_on',
                    models.DateTimeField(auto_now=True, db_index=True)
                ),
                (
                    'file',
                    models.FileField(
                        storage=veems.media.storage_backends.MediaFileStorage,
                        upload_to=veems.media.models.
                        _mediafile_segment_upload_to
                    )
                ),
                ('segment_number', models.IntegerField()),
                (
                    'media_file',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='media.mediafile'
                    )
                ),
            ],
            options={
                'unique_together': {('media_file', 'segment_number')},
            },
        ),
    ]