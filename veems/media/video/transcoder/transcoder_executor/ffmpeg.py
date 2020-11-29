import tempfile
import os
from pathlib import Path
import subprocess

from django.utils import timezone
from ffprobe import FFProbe

from .. import transcoder_profiles


def _get_metadata(video_path):
    metadata = FFProbe(str(video_path))
    first_stream = metadata.video[0]
    return {
        'width': int(first_stream.width),
        'height': int(first_stream.height),
    }


def _ffmpeg_transcode(
    source_file_path, bitrate, width, height, output_file_path
):
    command_template = (
        f'ffmpeg -y -i {source_file_path} '
        '-c:v libvpx-vp9 -crf 30 -b:v 0 '
        f'-b:a {bitrate}k '
        f'-vf scale={width}:{height} '
        '-c:a libopus '
        f'{output_file_path}'
    )
    result = os.system(command_template)
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
    tmp_dir = tempfile.mkdtemp()
    output_file_path = Path(tmp_dir) / profile.storage_filename
    try:
        _ffmpeg_transcode(
            source_file_path=source_file_path,
            width=profile.width,
            height=profile.height,
            bitrate=profile.bitrate,
            output_file_path=output_file_path,
        )
    except RuntimeError:
        transcode_job.status = 'failed'
        transcode_job.ended_on = timezone.now()
        return None
    else:
        transcode_job.status = 'completed'
        transcode_job.ended_on = timezone.now()
        return output_file_path
