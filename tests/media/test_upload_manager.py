import pytest

from veems.media import upload_manager, models

pytestmark = pytest.mark.django_db
MODULE = 'veems.media.upload_manager'


def test_prepare(user):
    upload, video = upload_manager.prepare(user=user, filename='MyFile.mp4')

    assert isinstance(upload, models.Upload)
    assert upload.media_type == 'video'
    assert upload.presigned_upload_url.startswith('http')
    assert upload.file
    assert isinstance(video, models.Video)
    assert not video.title
    assert video.visibility == 'draft'


class TestComplete:
    def test(self, video, mocker):
        mock_create_transcodes = mocker.patch(
            f'{MODULE}.transcode_manager.create_transcodes'
        )

        upload_manager.complete(upload_id=video.upload.id)

        assert mock_create_transcodes.called
        mock_create_transcodes.assert_called_once_with(video_id=video.id)
        video.refresh_from_db()
        assert video.upload.status == 'completed'

    def test_does_nothing_if_upload_status_completed(self, video, mocker):
        mock_create_transcodes = mocker.patch(
            f'{MODULE}.transcode_manager.create_transcodes'
        )
        video.upload.status = 'completed'
        video.upload.save()

        upload_manager.complete(upload_id=video.upload.id)

        assert not mock_create_transcodes.called
        assert video.upload.status == 'completed'


def test_get_presigned_upload_url(settings, user):
    filename = 'MyFile.mp4'
    upload = models.Upload.objects.create(user=user, media_type='video')

    signed_url, object_key = upload_manager._get_presigned_upload_url(
        upload=upload,
        filename=filename,
    )

    assert signed_url.startswith('http')
    assert 'AccessKeyId' in signed_url
    assert settings.BUCKET_MEDIA in signed_url
    assert object_key in signed_url
