from http.client import CREATED, BAD_REQUEST, OK
import json

import requests
import pytest

from veems.media import models
from tests import constants

pytestmark = pytest.mark.django_db
MODULE = 'veems.media.views'


class TestUploadPrepare:
    def test_put_with_filename_returns_upload_id(self, client, mocker):
        body = json.dumps({'filename': 'MyFile.mp4'})
        url = '/api/v1/upload/prepare/'

        response = client.put(url, body, content_type='application/json')

        assert response.status_code == CREATED
        assert models.Upload.objects.count() == 1
        assert models.Video.objects.count() == 1
        assert response.json() == {
            'upload_id': models.Upload.objects.first().id,
            'video_id': models.Video.objects.first().id,
            'presigned_upload_url': (
                models.Upload.objects.first().presigned_upload_url
            ),
        }

    def test_put_without_filename_returns_400(self, client):
        url = '/api/v1/upload/prepare/'

        response = client.put(url, content_type='application/json')

        assert response.status_code == BAD_REQUEST
        assert response.json() == {'detail': 'Filename not provided'}

    def test_put_with_invalid_filename_returns_400(self, client):
        body = json.dumps({'filename': 'MyFile'})
        url = '/api/v1/upload/prepare/'

        response = client.put(url, body, content_type='application/json')

        assert response.status_code == BAD_REQUEST
        assert response.json() == {'detail': 'Filename invalid'}


class TestUploadComplete:
    def test_put_with_upload_id_triggers_transcoding_process(
        self, client, settings, simple_uploaded_file
    ):

        body = json.dumps({'filename': constants.VID_240P_24FPS.name})
        url = '/api/v1/upload/prepare/'
        response = client.put(url, body, content_type='application/json')
        resp_json = response.json()
        upload_id = resp_json['upload_id']
        presigned_upload_url = resp_json['presigned_upload_url']

        # Upload the file completely outside of Django
        with constants.VID_240P_24FPS.open('rb') as data:
            resp = requests.put(presigned_upload_url, data)
        assert resp.ok, resp.text

        url = f'/api/v1/upload/complete/{upload_id}/'
        response = client.put(url, body, content_type='application/json')

        assert response.status_code == OK


class TestVideo:
    def test_get(
        self, client, video_factory, transcode_job_factory, mocker,
        simple_uploaded_file
    ):
        video = video_factory(
            video_path=constants.VIDEO_PATH_2160_30FPS,
            description='description',
            tags=['tag1', 'tag2'],
            visibility='draft',
            title='title',
        )
        transcode_job = transcode_job_factory(
            profile='360p', video_record=video
        )
        transcode_job2 = transcode_job_factory(
            profile='720p', video_record=video
        )
        media_file = models.MediaFile.objects.create(
            video=video,
            file=simple_uploaded_file,
            file_size=1000,
            width=320,
            height=240,
            duration=10,
            ext='webm',
            container='webm',
            audio_codec='opus',
            video_codec='vp9',
            name='240p',
            framerate=30,
        )

        response = client.get(f'/api/v1/video/{video.id}/')

        assert response.status_code == OK
        assert response.json() == {
            'description': 'description',
            'tags': ['tag1', 'tag2'],
            'title': 'title',
            'visibility': 'draft',
            # TODO: add playlist url
            'media_files': [
                {
                    'audio_codec': 'opus',
                    'container': 'webm',
                    'created_on': mocker.ANY,
                    'duration': 10,
                    'ext': 'webm',
                    # TODO: add presigned get url
                    'file': media_file.file.url,
                    'file_size': 1000,
                    'framerate': 30,
                    'height': 240,
                    'id': media_file.id,
                    'modified_on': mocker.ANY,
                    'name': '240p',
                    'video': video.id,
                    'video_codec': 'vp9',
                    'width': 320
                }
            ],
            'transcode_jobs': [
                {
                    'created_on': mocker.ANY,
                    'ended_on': None,
                    'executor': 'ffmpeg',
                    'failure_context': None,
                    'id': transcode_job.id,
                    'modified_on': mocker.ANY,
                    'profile': '360p',
                    'started_on': mocker.ANY,
                    'status': 'created',
                    'video': video.id
                },
                {
                    'created_on': mocker.ANY,
                    'ended_on': None,
                    'executor': 'ffmpeg',
                    'failure_context': None,
                    'id': transcode_job2.id,
                    'modified_on': mocker.ANY,
                    'profile': '720p',
                    'started_on': mocker.ANY,
                    'status': 'created',
                    'video': video.id
                },
            ],
        }
