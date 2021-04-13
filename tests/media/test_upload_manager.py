import pytest

from veems.media import upload_manager, models

pytestmark = pytest.mark.django_db
MODULE = 'veems.media.upload_manager'


def test_prepare(user, channel_factory):
    channel = channel_factory(user=user)
    num_parts = 10

    upload, video = upload_manager.prepare(
        user=user,
        filename='MyFile.mp4',
        channel_id=channel.id,
        num_parts=num_parts,
    )

    assert isinstance(upload, models.Upload)
    assert upload.media_type == 'video'
    assert len(upload.presigned_upload_urls) == num_parts
    for url in upload.presigned_upload_urls:
        assert url.startswith('http')
    assert upload.file
    assert isinstance(video, models.Video)
    assert video.title == 'MyFile'
    assert video.visibility == 'public'
    assert upload.channel == channel
    assert video.channel == channel
    assert video.filename == 'MyFile.mp4'
    assert upload.video == video


class TestComplete:
    @pytest.fixture
    def parts(self):
        return (
            {'etag': '123456789', 'part_number': '1'},
            {'etag': '123456789', 'part_number': '2'},
            {'etag': '123456789', 'part_number': '3'},
        )

    def test(self, user, channel_factory, mocker, parts):
        mock_create_transcodes = mocker.patch(
            f'{MODULE}.transcode_manager.create_transcodes'
        )
        channel = channel_factory(user=user)
        upload, video = upload_manager.prepare(
            user=user,
            filename='MyFile.mp4',
            channel_id=channel.id,
            num_parts=len(parts),
        )

        mock_provider_complete_multipart_upload = mocker.patch(
            f'{MODULE}._provider'
        )().complete_multipart_upload

        upload_manager.complete(upload_id=upload.id, parts=parts)

        assert mock_create_transcodes.called
        mock_create_transcodes.assert_called_once_with(video_id=video.id)
        video.refresh_from_db()
        upload.refresh_from_db()
        assert upload.status == 'uploaded'
        assert mock_provider_complete_multipart_upload.called
        mock_provider_complete_multipart_upload.assert_called_once_with(
            Bucket=upload.file.field.storage.bucket_name,
            Key=upload.file.name,
            MultipartUpload={
                'Parts': [
                    {'ETag': p['etag'], 'PartNumber': p['part_number']}
                    for p in parts
                ]
            },
            UploadId=upload.provider_upload_id,
        )

    def test_does_nothing_if_upload_status_completed(
        self,
        mocker,
        parts,
        user,
        channel_factory,
    ):
        mock_create_transcodes = mocker.patch(
            f'{MODULE}.transcode_manager.create_transcodes'
        )
        channel = channel_factory(user=user)
        upload, video = upload_manager.prepare(
            user=user,
            filename='MyFile.mp4',
            channel_id=channel.id,
            num_parts=len(parts),
        )
        upload.status = 'completed'
        upload.save()

        upload_manager.complete(upload_id=upload.id, parts=parts)

        assert not mock_create_transcodes.called
        upload.refresh_from_db()
        assert upload.status == 'completed'

    def test_does_nothing_if_upload_provider_upload_id_missing(
        self,
        mocker,
        parts,
        user,
        channel_factory,
    ):
        mock_create_transcodes = mocker.patch(
            f'{MODULE}.transcode_manager.create_transcodes'
        )
        channel = channel_factory(user=user)
        upload, video = upload_manager.prepare(
            user=user,
            filename='MyFile.mp4',
            channel_id=channel.id,
            num_parts=len(parts),
        )
        upload.provider_upload_id = None
        upload.save()

        upload_manager.complete(upload_id=upload.id, parts=parts)

        assert not mock_create_transcodes.called


def test_get_presigned_upload_url(settings, user, channel_factory):
    filename = 'MyFile.mp4'
    channel = channel_factory(user=user)
    upload = models.Upload.objects.create(channel=channel, media_type='video')

    (
        provider_upload_id,
        signed_urls,
        object_key,
    ) = upload_manager._get_presigned_upload_url(
        upload=upload,
        filename=filename,
        num_parts=5,
    )

    assert provider_upload_id
    for signed_url in signed_urls:
        assert signed_url.startswith('http')
        assert 'AccessKeyId' in signed_url
        assert settings.BUCKET_MEDIA in signed_url
        assert object_key in signed_url


@pytest.mark.parametrize(
    'filename, exp_title',
    [
        (
            'y2mate.com - we_need_to_talk_8OLxoiwE0Fc_1080p.mp4',
            'y2mate com we need to talk 8OLxoiwE0Fc 1080p',
        ),
    ],
)
def test_default_video_title_from_filename(filename, exp_title):
    result = upload_manager._default_video_title_from_filename(
        filename=filename
    )

    assert result == exp_title
