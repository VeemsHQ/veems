from pathlib import Path
import json

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.management.base import BaseCommand

from veems.channel import services as channel_services


def _run():
    seed_data = Path(settings.BASE_DIR / 'seed_data.json')
    with seed_data.open('r') as file_:
        data = json.load(file_)
    for row in data:
        user = get_user_model().objects.create(
            username=row['user']['username'],
            email=row['user']['email'],
        )
        user.set_password(row['user']['password'])
        user.save()
        for channel in row['channels']:
            channel_services.create_channel(
                name=channel['name'],
                description=channel['description'],
                sync_videos_interested=channel['sync_videos_interested'],
                language='en',
                user=user,
            )


class Command(BaseCommand):
    help = 'Imports Seed Data for Development Purposes'

    def handle(self, *args, **options):
        self.stdout.write('Seed data import started')
        _run()
        self.stdout.write('Seed data import completed')
