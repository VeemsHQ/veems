from pathlib import Path
import json
import io

import requests
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from veems.channel import services as channel_services
from veems.media import upload_manager


def _run():
    seed_data = Path(settings.BASE_DIR / 'seed_data.json')
    with seed_data.open('r') as file_:
        data = json.load(file_)
    for row in data:
        user = get_user_model()(
            username=row['user']['username'],
            email=row['user']['email'],
            is_staff=True,
            is_superuser=True,
        )
        user.set_password(row['user']['password'])
        user.save()
        for channel in row['channels']:
            channel_record = channel_services.create_channel(
                name=channel['name'],
                description=channel['description'],
                sync_videos_interested=channel['sync_videos_interested'],
                language='en',
                user=user,
            )
            print('Created Channel', channel_record.id)
            for video in channel['videos']:
                path = Path(video['path'])
                upload, video_record = upload_manager.prepare(
                    user=user, filename=path.name, channel_id=channel_record.id
                )
                video_record.title = video['title']
                video_record.description = video['description']
                video_record.save(update_fields=('title', 'description'))
                print('Created Video', video_record.id)
                with path.open('rb') as file_:
                    # Upload the file completely outside of Django
                    resp = requests.put(
                        upload.presigned_upload_url, io.BytesIO(file_.read())
                    )
                    resp.raise_for_status()
                    upload.file = File(file_)
                    upload.save(update_fields=('file',))
                upload_manager.complete(upload_id=upload.id)


class Command(BaseCommand):
    help = 'Imports Seed Data for Development Purposes'

    def handle(self, *args, **options):
        self.stdout.write('Seed data import started')
        _run()
        self.stdout.write('Seed data import completed')
