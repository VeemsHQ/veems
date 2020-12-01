import tempfile
import os
import logging
from pathlib import Path

from django.utils import timezone
from ffprobe import FFProbe

from .. import transcoder_profiles

logger = logging.getLogger(__name__)


def _get_metadata(video_path):
    metadata = FFProbe(str(video_path))
    first_stream = metadata.video[0]
    return {
        'width': int(first_stream.width),
        'height': int(first_stream.height),
        'framerate': int(first_stream.framerate),
    }


def _ffmpeg_transcode(*, source_file_path, profile, output_file_path):
    base_command = (
        f'ffmpeg -y -i {source_file_path} -vf '
        f'scale={profile.width}x{profile.height} '
        f'-b:v {profile.average_rate}k '
        f'-minrate {profile.min_rate}k '
        f'-maxrate {profile.max_rate}k '
        f'-tile-columns {profile.tile_columns} '
        '-g 240 '
        f'-threads {profile.threads} '
        '-quality good '
        f'-crf {profile.constant_rate_factor} '
        '-c:v libvpx-vp9 '
        '-c:a libopus '
        '-speed 4 '
    )
    command_1 = base_command + ('-pass 1 ' f'{output_file_path}')
    command_2 = base_command + ('-pass 2 ' f'{output_file_path}')
    result = os.system(command_1)
    if result != 0:
        raise RuntimeError('Transcoding failed')
    result = os.system(command_2)
    if result != 0:
        raise RuntimeError('Transcoding failed')


def transcode(*, transcode_job, source_file_path):
    """

    TODOs

    1. open the video file with ffmpeg
    2. extract the first video stream.
    3. get the width and height of the video
    4. (not always) if the video is vertical, rotate it.
    5. run the transcode with ffmpeg
    6. upload the resulting webm file to s3 bucket/others
    7. update the transcode job status = COMPLETE
    """
    profile = [
        p for p in transcoder_profiles.PROFILES
        if p.name == transcode_job.profile
    ][0]
    metadata = _get_metadata(source_file_path)
    if profile.height > metadata['height']:
        _mark_completed(transcode_job)
        return None
    if not (
        profile.min_framerate <= metadata['framerate'] <= profile.max_framerate
    ):
        _mark_completed(transcode_job)
        return None

    tmp_dir = tempfile.mkdtemp()
    output_file_path = Path(tmp_dir) / profile.storage_filename
    if not source_file_path.exists():
        raise LookupError('Source file not found')
    try:
        _ffmpeg_transcode(
            source_file_path=source_file_path,
            profile=profile,
            output_file_path=output_file_path,
        )
    except RuntimeError:
        _mark_failed(transcode_job)
        return None
    else:
        _mark_completed(transcode_job)
        return output_file_path


def _mark_completed(transcode_job):
    transcode_job.status = 'completed'
    transcode_job.ended_on = timezone.now()


def _mark_failed(transcode_job):
    transcode_job.status = 'failed'
    transcode_job.ended_on = timezone.now()
