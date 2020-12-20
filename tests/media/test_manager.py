import logging

import pytest
from django.utils import timezone
from ffprobe import FFProbe

from veems.media import models
from veems.media.transcoder import manager
from veems.media.transcoder import transcoder_profiles
from tests import constants

pytestmark = pytest.mark.django_db

MODULE = 'veems.media.transcoder.manager'


@pytest.mark.parametrize(
    'video_path, exp_profiles', [
        (
            constants.VID_2160P_30FPS,
            [
                'webm_144p', 'webm_240p', 'webm_360p', 'webm_720p',
                'webm_1080p', 'webm_1440p', 'webm_2160p'
            ],
        ),
        (
            constants.VID_2160P_24FPS,
            [
                'webm_144p', 'webm_240p', 'webm_360p', 'webm_720p',
                'webm_1080p', 'webm_1440p', 'webm_2160p'
            ],
        ),
        (
            constants.VID_720P_24FPS,
            [
                'webm_144p',
                'webm_240p',
                'webm_360p',
                'webm_720p',
            ],
        ),
        (
            constants.VID_1828_X_1332_24FPS,
            [
                'webm_144p',
                'webm_240p',
                'webm_360p',
                'webm_720p',
                'webm_1080p',
            ],
        ),
        (
            constants.VID_1440P_24FPS,
            [
                'webm_144p',
                'webm_240p',
                'webm_360p',
                'webm_720p',
                'webm_1080p',
                'webm_1440p',
            ],
        ),
        (
            constants.VID_360P_24FPS,
            [
                'webm_144p',
                'webm_240p',
                'webm_360p',
            ],
        ),
        (
            constants.VID_240P_24FPS,
            [
                'webm_144p',
                'webm_240p',
            ],
        ),
        (
            constants.VIDEO_PATH_1080_30FPS_VERT,
            [
                'webm_144p',
                'webm_240p',
                'webm_360p',
                'webm_720p',
                'webm_1080p',
            ],
        ),
        (
            constants.VID_1920_X_960,
            [
                'webm_144p',
                'webm_240p',
                'webm_360p',
                'webm_720p',
                'webm_1080p',
            ],
        ),
    ]
)
def test_get_applicable_transcode_profiles(video_path, exp_profiles):
    profiles = manager._get_applicable_transcode_profiles(
        video_path=video_path
    )

    assert [p.name for p in profiles] == exp_profiles


@pytest.mark.parametrize(
    'video_filename, profile_cls, exp_result', [
        ('2160p_30fps.mp4', transcoder_profiles.Webm360p, True),
        ('2160p_30fps.mp4', transcoder_profiles.Webm720p, True),
        ('2160p_30fps.mp4', transcoder_profiles.Webm1080p, True),
        ('2160p_30fps.mp4', transcoder_profiles.Webm2160p, True),
        ('2160p_30fps.mp4', transcoder_profiles.Webm720pHigh, False),
        ('2160p_30fps.mp4', transcoder_profiles.Webm1080pHigh, False),
        ('2160p_30fps.mp4', transcoder_profiles.Webm2160pHigh, False),
        ('360p_60fps.webm', transcoder_profiles.Webm360pHigh, True),
        ('360p_60fps.webm', transcoder_profiles.Webm360p, False),
        ('360p_60fps.webm', transcoder_profiles.Webm720p, False),
        ('360p_60fps.webm', transcoder_profiles.Webm720pHigh, False),
        ('360p_60fps.webm', transcoder_profiles.Webm1080p, False),
        ('360p_60fps.webm', transcoder_profiles.Webm1080pHigh, False),
        ('360p_60fps.webm', transcoder_profiles.Webm2160p, False),
        ('360p_60fps.webm', transcoder_profiles.Webm2160pHigh, False),
        ('1080p_60fps.mp4', transcoder_profiles.Webm360pHigh, True),
        ('1080p_60fps.mp4', transcoder_profiles.Webm720pHigh, True),
        ('1080p_60fps.mp4', transcoder_profiles.Webm1080pHigh, True),
        ('1080p_60fps.mp4', transcoder_profiles.Webm2160pHigh, False),
        ('1080p_60fps.mp4', transcoder_profiles.Webm360p, False),
        ('1080p_60fps.mp4', transcoder_profiles.Webm720p, False),
        ('1080p_60fps.mp4', transcoder_profiles.Webm1080p, False),
        ('1080p_60fps.mp4', transcoder_profiles.Webm2160p, False),
    ]
)
def test_transcode_profile_does_apply(video_filename, profile_cls, exp_result):
    video_path = constants.TEST_DATA_DIR / video_filename
    metadata = FFProbe(str(video_path))
    ffprobe_stream = metadata.video[0]

    result = manager._transcode_profile_does_apply(
        profile_cls=profile_cls, ffprobe_stream=ffprobe_stream
    )

    assert result == exp_result


@pytest.mark.xfail
@pytest.mark.parametrize(
    'video_filename, exp_profiles',
    [
        (
            constants.VID_720P_24FPS, (
                'webm_144p',
                'webm_240p',
                'webm_360p',
                'webm_720p',
            )
        ),
        (
            constants.VIDEO_PATH_360_60FPS, (
                'webm_144p',
                'webm_240p',
                'webm_360p_high',
            )
        ),
    ]
)
def test_create_transcodes(
    video_filename, exp_profiles, video_factory, mocker, settings
):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    video = video_factory(video_path=video_filename)

    async_result = manager.create_transcodes(video_id=video.id)

    assert async_result.state == 'SUCCESS'

    # When transcoding is completed, the video and mediafiles under it
    # should all have playlists generated for them.
    video.refresh_from_db()
    assert video.playlist_file
    for media_file in video.mediafile_set.all():
        assert media_file.playlist_file

    exp_num_jobs = len(exp_profiles)
    executed_profiles = tuple(
        models.TranscodeJob.objects.values_list('profile', flat=True)
    )
    assert (
        models.TranscodeJob.objects.filter(status='completed'
                                           ).count() == exp_num_jobs
    )
    assert executed_profiles == exp_profiles


class TestTaskOnAllTranscodesCompleted:
    def test(self, video, mocker):
        mock_update_video_master_playlist = mocker.patch(
            f'{MODULE}.services.update_video_master_playlist'
        )

        manager.task_on_all_transcodes_completed(
            task_results=True, video_id=video.id
        )

        assert mock_update_video_master_playlist.called

    def test_logs_warning_if_not_all_task_results_successful(
        self, video, mocker, caplog
    ):
        mock_update_video_master_playlist = mocker.patch(
            f'{MODULE}.services.update_video_master_playlist'
        )
        caplog.set_level(logging.WARNING)

        manager.task_on_all_transcodes_completed(
            task_results=None, video_id=video.id
        )

        assert mock_update_video_master_playlist.called
        assert (
            f'Not all transcodes successful for Video {video.id}'
            in caplog.messages
        )


def test_task_transcode(video_factory, mocker):
    video = video_factory(video_path=constants.VID_360P_24FPS)
    mock_executor = mocker.patch(f'{MODULE}.transcode_executor')
    transcode_job = models.TranscodeJob.objects.create(
        video=video,
        profile='webm_360p_high',
        executor='ffmpeg',
        status='created',
        started_on=timezone.now(),
    )

    manager.task_transcode(
        video_id=video.id, transcode_job_id=transcode_job.id
    )

    mock_executor.transcode.assert_called_once_with(
        transcode_job=transcode_job,
        source_file_path=mocker.ANY,
    )
    transcode_job.refresh_from_db()
    assert transcode_job.status == 'processing'
    assert transcode_job.started_on
    # Check that the file sent to the transcode job
    # is the uploaded file.
    source_file_path = (
        mock_executor.transcode.call_args.kwargs['source_file_path']
    )
    with source_file_path.open('rb') as file_:
        file_data = file_.read()
    assert file_data == video.upload.file.read()
