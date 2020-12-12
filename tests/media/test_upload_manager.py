import pytest

from veems.media import upload_manager, models

pytestmark = pytest.mark.django_db
MODULE = 'veems.media.upload_manager'


def test_prepare():
    upload, video = upload_manager.prepare(filename='MyFile.mp4')

    assert isinstance(upload, models.Upload)
    assert upload.media_type == 'video'
    assert upload.presigned_upload_url.startswith('http')
    assert isinstance(video, models.Video)
    assert not video.title
    assert video.visibility == 'draft'


def test_complete(video, mocker):
    mock_create_transcodes = mocker.patch(
        f'{MODULE}.transcode_manager.create_transcodes'
    )

    upload_manager.complete(upload_id=video.upload.id)

    assert mock_create_transcodes.called
    mock_create_transcodes.assert_called_once_with(video_id=video.id)


def test_get_presigned_upload_url(settings):
    filename = 'MyFile.mp4'
    upload = models.Upload.objects.create(media_type='video')

    signed_url = upload_manager._get_presigned_upload_url(
        upload=upload,
        filename=filename,
    )

    assert signed_url.startswith('http')
    assert 'AccessKeyId' in signed_url
    assert settings.BUCKET_UPLOADS in signed_url
