import pytest

from veems.media import upload_manager, models

pytestmark = pytest.mark.django_db


def test_prepare():
    upload, video = upload_manager.prepare()

    assert isinstance(upload, models.Upload)
    assert upload.media_type == 'video'
    assert upload.presigned_upload_url.startswith('https://')
    assert isinstance(video, models.Video)
    assert not upload.title


def test_complete(upload):
    upload_manager.complete(upload_id=upload.id)
