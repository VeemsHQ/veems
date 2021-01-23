import pytest

from veems.media import upload_manager, models

pytestmark = pytest.mark.django_db
MODULE = 'veems.media.upload_manager'


def test_prepare(user, channel_factory):
    channel = channel_factory(user=user)

    upload, video = upload_manager.prepare(
        user=user, filename='MyFile.mp4', channel_id=channel.id
    )

    assert isinstance(upload, models.Upload)
    assert upload.media_type == 'video'
    assert upload.presigned_upload_url.startswith('http')
    assert upload.file
    assert isinstance(video, models.Video)
    assert video.visibility == 'public'
    assert upload.channel == channel
    assert video.channel == channel
    assert video.title == 'MyFile'


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


def test_get_presigned_upload_url(settings, user, channel_factory):
    filename = 'MyFile.mp4'
    channel = channel_factory(user=user)
    upload = models.Upload.objects.create(channel=channel, media_type='video')

    signed_url, object_key = upload_manager._get_presigned_upload_url(
        upload=upload,
        filename=filename,
    )

    assert signed_url.startswith('http')
    assert 'AccessKeyId' in signed_url
    assert settings.BUCKET_MEDIA in signed_url
    assert object_key in signed_url


@pytest.mark.parametrize(
    'filename, exp_title',
    [
        (
            'y2mate.com - we_need_to_talk_8OLxoiwE0Fc_1080p.mp4',
            'y2mate com   we need to talk 8OLxoiwE0Fc 1080p',
        ),
    ],
)
def test_default_video_title_from_filename(filename, exp_title):
    result = upload_manager._default_video_title_from_filename(
        filename=filename
    )

    assert result == exp_title
