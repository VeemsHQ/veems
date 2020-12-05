import pytest

from veems.media import upload_manager, models

pytestmark = pytest.mark.django_db
MODULE = 'veems.media.upload_manager'


def test_prepare():
    upload, video = upload_manager.prepare()

    assert isinstance(upload, models.Upload)
    assert upload.media_type == 'video'
    assert upload.presigned_upload_url.startswith('https://')
    assert isinstance(video, models.Video)
    assert not video.title


def test_complete(video, mocker):
    mock_create_transcodes = mocker.patch(
        f'{MODULE}.transcode_manager.create_transcodes'
    )

    upload_manager.complete(upload_id=video.upload.id)

    assert mock_create_transcodes.called
    mock_create_transcodes.assert_called_once_with(
        video_id=video.id
    )
