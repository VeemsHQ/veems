from http.client import CREATED, BAD_REQUEST, OK, NO_CONTENT
import json

import pytest
import m3u8

from veems.media import models, services
from tests import constants

pytestmark = pytest.mark.django_db
MODULE = 'veems.media.api_views'
VIDEO_PATH = constants.VID_360P_24FPS


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
        self, client, settings, mocker
    ):
        body = json.dumps({'filename': VIDEO_PATH.name})
        url = '/api/v1/upload/prepare/'
        response = client.put(url, body, content_type='application/json')
        resp_json = response.json()
        upload_id = resp_json['upload_id']
        mock_upload_manager = mocker.patch(f'{MODULE}.upload_manager')

        url = f'/api/v1/upload/complete/{upload_id}/'
        response = client.put(url, body, content_type='application/json')

        assert response.status_code == OK

        assert mock_upload_manager.complete.delay.called
        mock_upload_manager.complete.delay.assert_called_once_with(upload_id)


class TestVideo:
    def test_get(
        self, client, video_factory, transcode_job_factory, mocker,
        simple_uploaded_file_factory, rendition_playlist_file
    ):
        video = video_factory(
            video_path=VIDEO_PATH,
            description='description',
            tags=['tag1', 'tag2'],
            visibility='draft',
            title='title',
        )
        transcode_job = transcode_job_factory(
            profile='144p', video_record=video
        )
        transcode_job2 = transcode_job_factory(
            profile='360p', video_record=video
        )
        file_ = simple_uploaded_file_factory(video_path=VIDEO_PATH)
        media_file = models.MediaFile.objects.create(
            video=video,
            file=file_,
            playlist_file=rendition_playlist_file,
            file_size=1000,
            width=256,
            height=144,
            duration=10,
            ext='webm',
            container='webm',
            audio_codec='opus',
            video_codec='vp9',
            name='144p',
            framerate=30,
            metadata={'example': 'metadata'},
        )

        response = client.get(f'/api/v1/video/{video.id}/')

        assert response.status_code == OK
        assert response.json() == {
            'description': 'description',
            'tags': ['tag1', 'tag2'],
            'title': 'title',
            'visibility': 'draft',
            'playlist_file': f'/api/v1/video/{video.id}/playlist.m3u8',
            'media_files': [
                {
                    'audio_codec': 'opus',
                    'container': 'webm',
                    'codecs_string': None,
                    'playlist_file': mocker.ANY,
                    'created_on': mocker.ANY,
                    'duration': 10,
                    'ext': 'webm',
                    'file_size': 1000,
                    'framerate': 30,
                    'height': 144,
                    'id': media_file.id,
                    'metadata': {
                        'example': 'metadata'
                    },
                    'modified_on': mocker.ANY,
                    'name': '144p',
                    'video': video.id,
                    'video_codec': 'vp9',
                    'width': 256
                }
            ],
            'transcode_jobs': [
                {
                    'created_on': mocker.ANY,
                    'ended_on': None,
                    'executor': 'ffmpeg',
                    'id': transcode_job.id,
                    'modified_on': mocker.ANY,
                    'profile': '144p',
                    'started_on': mocker.ANY,
                    'status': 'created',
                    'video': video.id
                },
                {
                    'created_on': mocker.ANY,
                    'ended_on': None,
                    'executor': 'ffmpeg',
                    'id': transcode_job2.id,
                    'modified_on': mocker.ANY,
                    'profile': '360p',
                    'started_on': mocker.ANY,
                    'status': 'created',
                    'video': video.id
                },
            ],
        }


class TestVideoPlaylist:
    def test_get(
        self, client, video_factory, transcode_job_factory, mocker,
        simple_uploaded_file_factory, rendition_playlist_file
    ):
        video = video_factory(
            video_path=VIDEO_PATH,
            description='description',
            tags=['tag1', 'tag2'],
            visibility='draft',
            title='title',
        )
        file_ = simple_uploaded_file_factory(video_path=VIDEO_PATH)
        models.MediaFile.objects.create(
            video=video,
            file=file_,
            playlist_file=rendition_playlist_file,
            file_size=1000,
            width=256,
            height=144,
            duration=10,
            ext='webm',
            container='webm',
            audio_codec='opus',
            video_codec='vp9',
            name='144p',
            framerate=30,
            metadata=services.get_metadata(VIDEO_PATH),
        )

        response = client.get(f'/api/v1/video/{video.id}/playlist.m3u8')

        assert response.status_code == OK
        resp_text = response.content.decode()
        assert resp_text.startswith('#EXTM3U')
        assert m3u8.loads(resp_text).data == {
            'iframe_playlists': [],
            'is_endlist': False,
            'is_i_frames_only': False,
            'is_independent_segments': False,
            'is_variant': True,
            'keys': [],
            'media': [],
            'media_sequence': None,
            'part_inf': {},
            'playlist_type': None,
            'playlists': [
                {
                    'stream_info': {
                        'bandwidth': 182464,
                        'closed_captions': 'NONE',
                        'program_id': 1,
                        'resolution': '256x144'
                    },
                    'uri': mocker.ANY
                }
            ],
            'rendition_reports': [],
            'segments': [],
            'session_data': [],
            'session_keys': [],
            'skip': {}
        }

    def test_get_returns_204_if_video_has_no_renditions(self, client, video):
        response = client.get(f'/api/v1/video/{video.id}/playlist.m3u8')

        assert response.status_code == NO_CONTENT
        assert response.content.decode() == ''
