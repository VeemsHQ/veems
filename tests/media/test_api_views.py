from http.client import (
    CREATED,
    BAD_REQUEST,
    OK,
    NO_CONTENT,
    FORBIDDEN,
    NOT_FOUND,
)
import json

import pytest
import m3u8

from veems.media import models, services
from tests import constants

pytestmark = pytest.mark.django_db
MODULE = 'veems.media.api_views'
VIDEO_PATH = constants.VID_360P_24FPS


class TestUploadPrepare:
    URL = '/api/v1/upload/prepare/'

    def test_returns_403_when_auth_headers_not_provided(
        self, api_client_no_auth, channel
    ):
        api_client = api_client_no_auth
        body = json.dumps({'filename': 'MyFile.mp4', 'channel_id': channel.id})

        response = api_client.put(
            self.URL, body, content_type='application/json'
        )

        assert response.status_code == FORBIDDEN
        assert models.Upload.objects.count() == 0
        assert models.Video.objects.count() == 0

    def test_put_with_filename_returns_upload_id(
        self, api_client, channel_factory
    ):
        api_client, user = api_client
        channel = channel_factory(user=user)
        body = json.dumps({'filename': 'MyFile.mp4', 'channel_id': channel.id})

        response = api_client.put(
            self.URL, body, content_type='application/json'
        )

        assert response.status_code == CREATED
        assert models.Upload.objects.filter(channel__user=user).count() == 1
        assert models.Video.objects.filter(channel__user=user).count() == 1
        assert response.json() == {
            'upload_id': models.Upload.objects.first().id,
            'video_id': models.Video.objects.first().id,
            'presigned_upload_url': (
                models.Upload.objects.first().presigned_upload_url
            ),
        }

    def test_returns_404_when_attempting_to_upload_to_another_users_channel(
        self, user_factory, api_client, channel_factory
    ):
        api_client, user = api_client
        another_user = user_factory()
        channel = channel_factory(user=another_user)
        body = json.dumps({'filename': 'MyFile.mp4', 'channel_id': channel.id})

        response = api_client.put(
            self.URL, body, content_type='application/json'
        )

        assert response.status_code == NOT_FOUND
        assert response.json() == {'detail': 'Not found.'}

    def test_put_without_channel_id_returns_400(
        self,
        api_client,
    ):
        api_client, user = api_client
        body = json.dumps({'filename': 'MyFile.mp4'})

        response = api_client.put(
            self.URL, body, content_type='application/json'
        )

        assert response.status_code == BAD_REQUEST
        assert response.json() == {'detail': 'channel_id not provided'}

    def test_put_without_filename_returns_400(
        self, api_client, channel_factory
    ):
        api_client, user = api_client
        channel = channel_factory(user=user)
        body = json.dumps({'channel_id': channel.id})

        response = api_client.put(
            self.URL, body, content_type='application/json'
        )

        assert response.status_code == BAD_REQUEST
        assert response.json() == {'detail': 'Filename not provided'}

    def test_put_with_invalid_filename_returns_400(
        self, api_client, channel_factory
    ):
        api_client, user = api_client
        channel = channel_factory(user=user)
        body = json.dumps({'filename': 'MyFile', 'channel_id': channel.id})

        response = api_client.put(
            self.URL, body, content_type='application/json'
        )

        assert response.status_code == BAD_REQUEST
        assert response.json() == {'detail': 'Filename invalid'}


class TestUploadComplete:
    @pytest.fixture
    def upload_id(self, api_client, channel_factory):
        api_client, user = api_client
        channel = channel_factory(user=user)
        body = json.dumps(
            {'filename': VIDEO_PATH.name, 'channel_id': channel.id}
        )
        url = '/api/v1/upload/prepare/'
        response = api_client.put(url, body, content_type='application/json')
        resp_json = response.json()
        return resp_json['upload_id']

    def test_put_with_upload_id_triggers_transcoding_process(
        self, api_client, settings, mocker, upload_id, channel_factory
    ):
        api_client, user = api_client
        channel = channel_factory(user=user)
        mock_upload_manager = mocker.patch(f'{MODULE}.upload_manager')
        body = json.dumps(
            {'filename': VIDEO_PATH.name, 'channel_id': channel.id}
        )

        url = f'/api/v1/upload/complete/{upload_id}/'
        response = api_client.put(url, body, content_type='application/json')

        assert response.status_code == OK

        assert mock_upload_manager.complete.delay.called
        mock_upload_manager.complete.delay.assert_called_once_with(upload_id)

    def test_returns_404_when_user_attempts_to_complete_another_users_upload(
        self, upload_id, api_client_factory
    ):
        another_user_api_client, _ = api_client_factory()
        body = json.dumps({'filename': VIDEO_PATH.name})

        url = f'/api/v1/upload/complete/{upload_id}/'
        response = another_user_api_client.put(
            url, body, content_type='application/json'
        )

        assert response.status_code == NOT_FOUND
        assert response.json() == {'detail': 'Not found.'}

    def test_returns_403_when_auth_headers_not_provided(
        self, api_client_no_auth, upload_id
    ):
        body = json.dumps({'filename': 'MyFile.mp4'})

        url = f'/api/v1/upload/complete/{upload_id}/'
        response = api_client_no_auth.put(
            url, body, content_type='application/json'
        )

        assert response.status_code == FORBIDDEN


class TestVideoDetail:
    @pytest.fixture
    def video_with_transcodes(
        self,
        video_with_transcodes_factory,
        api_client_factory,
        channel,
    ):
        video_data = video_with_transcodes_factory(channel=channel)
        api_client, _ = api_client_factory(user=video_data['user'])
        return {**video_data, **{'api_client': api_client}}

    @pytest.fixture
    def expected_video_resp_json(self, video_with_transcodes, mocker):
        video = video_with_transcodes['video']
        transcode_job = video_with_transcodes['transcode_job']
        transcode_job2 = video_with_transcodes['transcode_job2']
        video_rendition = video_with_transcodes['video_rendition']
        return {
            'id': video.id,
            'channel': video.channel.id,
            'description': 'description',
            'tags': ['tag1', 'tag2'],
            'title': 'title',
            'visibility': 'draft',
            'playlist_file': f'/api/v1/video/{video.id}/playlist.m3u8',
            'video_renditions': [
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
                    'id': video_rendition.id,
                    'metadata': {'example': 'metadata'},
                    'modified_on': mocker.ANY,
                    'name': '144p',
                    'video': video.id,
                    'video_codec': 'vp9',
                    'width': 256,
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
                    'video': video.id,
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
                    'video': video.id,
                },
            ],
        }

    def test_get(
        self,
        api_client_no_auth,
        mocker,
        video_with_transcodes,
        expected_video_resp_json,
    ):
        video = video_with_transcodes['video']

        response = api_client_no_auth.get(f'/api/v1/video/{video.id}/')

        assert response.status_code == OK
        assert response.json() == expected_video_resp_json

    def test_put(
        self, mocker, video_with_transcodes, expected_video_resp_json
    ):
        video = video_with_transcodes['video']
        api_client = video_with_transcodes['api_client']

        payload = {
            'title': 'new title',
            'visibility': 'public',
            'description': 'new description',
            'tags': ['new', 'tags'],
        }
        response = api_client.put(
            f'/api/v1/video/{video.id}/',
            payload,
            format='json',
        )

        assert response.status_code == OK
        expected_video_resp_json.update(payload)
        assert response.json() == expected_video_resp_json

    def test_put_cannot_update_channel(
        self,
        video_with_transcodes,
        channel_factory,
        user_factory,
    ):
        video = video_with_transcodes['video']
        api_client = video_with_transcodes['api_client']
        other_users_channel = channel_factory(user=user_factory())

        response = api_client.put(
            f'/api/v1/video/{video.id}/',
            {
                'channel': other_users_channel.id,
            },
            format='json',
        )

        assert response.status_code == BAD_REQUEST

    def test_put_cannot_update_upload(
        self,
        video_with_transcodes,
        channel_factory,
        user_factory,
        upload_factory,
    ):
        video = video_with_transcodes['video']
        api_client = video_with_transcodes['api_client']
        other_users_channel = channel_factory(user=user_factory())
        other_upload = upload_factory(channel_=other_users_channel)

        response = api_client.put(
            f'/api/v1/video/{video.id}/',
            {
                'upload': other_upload.id,
            },
            format='json',
        )

        assert response.status_code == BAD_REQUEST

    def test_put_cannot_update_another_users_video(
        self,
        mocker,
        video_with_transcodes,
        channel_factory,
        user_factory,
        api_client_factory,
    ):
        video = video_with_transcodes['video']
        other_user_api_client, _ = api_client_factory(user=user_factory())

        response = other_user_api_client.put(
            f'/api/v1/video/{video.id}/',
            {
                'title': 'new title',
            },
            format='json',
        )

        assert response.status_code == NOT_FOUND

    def test_put_without_auth_returns_403(
        self,
        api_client_no_auth,
        video_with_transcodes,
    ):
        video = video_with_transcodes['video']

        response = api_client_no_auth.put(
            f'/api/v1/video/{video.id}/',
            {
                'title': 'new title',
            },
            format='json',
        )

        assert response.status_code == FORBIDDEN


class TestVideoPlaylist:
    def test_get(
        self,
        api_client_no_auth,
        video_factory,
        transcode_job_factory,
        mocker,
        simple_uploaded_file_factory,
        rendition_playlist_file,
    ):
        video = video_factory(
            video_path=VIDEO_PATH,
            description='description',
            tags=['tag1', 'tag2'],
            visibility='draft',
            title='title',
        )
        file_ = simple_uploaded_file_factory(video_path=VIDEO_PATH)
        models.VideoRendition.objects.create(
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

        response = api_client_no_auth.get(
            f'/api/v1/video/{video.id}/playlist.m3u8'
        )

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
                        'resolution': '256x144',
                    },
                    'uri': mocker.ANY,
                }
            ],
            'rendition_reports': [],
            'segments': [],
            'session_data': [],
            'session_keys': [],
            'skip': {},
        }

    def test_get_returns_204_if_video_has_no_renditions(
        self, api_client_no_auth, video
    ):
        response = api_client_no_auth.get(
            f'/api/v1/video/{video.id}/playlist.m3u8'
        )

        assert response.status_code == NO_CONTENT
        assert response.content.decode() == ''
