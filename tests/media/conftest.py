from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
import pytest

from veems.media.transcoder import transcoder_profiles
from veems.media.transcoder.transcoder_executor import ffmpeg
from veems.media import models, services
from tests import constants

TEST_DATA_DIR = Path(__file__).parent.parent / 'test_data'
VIDEO_PATH_2160_30FPS = TEST_DATA_DIR / '2160p_30fps.mp4'
EXAMPLE_IMG = TEST_DATA_DIR / 'example-image.jpeg'


@pytest.fixture
def upload(upload_factory):
    return upload_factory(video_path=VIDEO_PATH_2160_30FPS)


@pytest.fixture
def video(video_factory):
    return video_factory(video_path=VIDEO_PATH_2160_30FPS)


@pytest.fixture
def simple_uploaded_file():
    with VIDEO_PATH_2160_30FPS.open('rb') as file_:
        file_contents = file_.read()
    return SimpleUploadedFile(VIDEO_PATH_2160_30FPS.name, file_contents)


@pytest.fixture
def rendition_playlist_file():
    with constants.RENDITION_PLAYLIST.open('rb') as file_:
        file_contents = file_.read()
    return SimpleUploadedFile(constants.RENDITION_PLAYLIST.name, file_contents)


@pytest.fixture
def simple_uploaded_file_factory():
    def make(video_path):

        with video_path.open('rb') as file_:
            file_contents = file_.read()
        return SimpleUploadedFile(VIDEO_PATH_2160_30FPS.name, file_contents)

    return make


@pytest.fixture
def upload_factory(channel):
    def make(video_path=VIDEO_PATH_2160_30FPS, channel_=None):
        with video_path.open('rb') as file_:
            file_contents = file_.read()
        channel_ = channel_ or channel
        upload = models.Upload.objects.create(
            presigned_upload_url='htts://example.com/s3-blah',
            media_type='video',
            file=SimpleUploadedFile(video_path.name, file_contents),
            channel=channel_,
        )
        return upload

    return make


@pytest.fixture
def video_factory(upload_factory, channel):
    def make(video_path, **kwargs):
        upload = upload_factory(video_path=video_path)
        return models.Video.objects.create(
            upload=upload, channel=channel, **kwargs
        )

    return make


@pytest.fixture
def transcode_job_factory(video):
    def make(profile, status='created', video_record=None):
        return models.TranscodeJob.objects.create(
            video=video_record or video,
            profile=profile,
            executor='ffmpeg',
            status=status,
            started_on=timezone.now(),
        )

    return make


@pytest.fixture
def transcode_job(transcode_job_factory):
    return transcode_job_factory(profile='webm_360p')


@pytest.fixture
def video_with_renditions_and_segments(video, simple_uploaded_file, tmpdir):
    video_renditions_to_create = (
        (640, 360, constants.VID_360P_24FPS, False),
        (640, 360, constants.VID_360P_24FPS, True),
        (1920, 1080, constants.VIDEO_PATH_1080_60FPS, True),
    )
    for (
        width,
        height,
        video_path,
        create_segments,
    ) in video_renditions_to_create:
        video_rendition = models.VideoRendition.objects.create(
            video=video,
            file=simple_uploaded_file,
            name=f'{height}p',
            ext='webm',
            framerate=30,
            file_size=1,
            width=width,
            height=height,
            metadata=services.get_metadata(video_path),
            codecs_string='avc1.640028,mp4a.40.2',
        )
        assert not video_rendition.playlist_file
        if not create_segments:
            continue
        video_path = constants.VIDEO_PATH_1080_30FPS_VERT
        profile = transcoder_profiles.Webm360p
        (
            segments_playlist_file,
            segment_paths,
            _,
        ) = ffmpeg._create_segments_for_video(
            video_path=video_path,
            profile=profile,
            tmp_dir=tmpdir,
            video_rendition_id=video_rendition.id,
            video_id=video_rendition.video_id,
        )
        services.persist_video_rendition_segments(
            video_rendition=video_rendition,
            segments_playlist_file=segments_playlist_file,
            segments=segment_paths,
        )
    return video, video_renditions_to_create
