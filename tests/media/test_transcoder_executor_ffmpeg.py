from pathlib import Path

from django.utils import timezone
import pytest

from veems.media.video.transcoder.transcoder_executor import ffmpeg
from veems.media.models import TranscodeJob, Upload

pytestmark = pytest.mark.django_db
VIDEO_PATH = Path(__file__).parent.parent / 'test_data/1080p.mp4'


def test_get_metadata():
    metadata = ffmpeg._get_metadata(video_path=VIDEO_PATH)

    assert metadata == {
        'width': 1920,
        'height': 1080,
    }



def test_transcode():
    upload = Upload.objects.create(media_type='video/mp4')
    transcode_job = TranscodeJob.objects.create(
        upload=upload, profile='webm360p', executor='ffmpeg',
        status='created', started_on=timezone.now(),
    )

    result_path = ffmpeg.transcode(transcode_job=transcode_job, source_file_path=VIDEO_PATH)

    assert isinstance(result_path, Path)
    metadata = ffmpeg._get_metadata(video_path=result_path)
    assert metadata == {
        'width': 640,
        'height': 360,
    }
    # assert transcode_job.status == 'completed'
    # assert transcode_job.ended_on


