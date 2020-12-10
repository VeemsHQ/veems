from http.client import CREATED, BAD_REQUEST, OK
import json

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
        self, client, settings, simple_uploaded_file, mocker
    ):

        body = json.dumps({'filename': constants.VID_240P_24FPS.name})
        url = '/api/v1/upload/prepare/'
        response = client.put(url, body, content_type='application/json')
        resp_json = response.json()
        upload_id = resp_json['upload_id']

        # Upload the Video file to S3
        upload = models.Upload.objects.get(id=upload_id)
        upload.file = simple_uploaded_file
        upload.save()
        # TODO: upload file using s3 PUT api
        # Upload the file completely outside of Django
        # with constants.VID_240P_24FPS.open('rb') as data:
        #  resp = requests.post(presigned_upload_url, data)
        # assert resp.ok, resp.textField
        mock_upload_manager = mocker.patch(f'{MODULE}.upload_manager')

        url = f'/api/v1/upload/complete/{upload_id}/'
        response = client.put(url, body, content_type='application/json')

        assert response.status_code == OK

        assert mock_upload_manager.complete.delay.called
        mock_upload_manager.complete.delay.assert_called_once_with(upload_id)
