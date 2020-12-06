import tempfile
import os
import time
import logging
from pathlib import Path

from django.core.files import File
from django.utils import timezone
from ffprobe import FFProbe

from .. import transcoder_profiles
from .... import models

logger = logging.getLogger(__name__)


def transcode(*, transcode_job, source_file_path):
    """

    TODOs

    1. open the video file with ffmpeg
    2. extract the first video stream.
    3. get the width and height of the video
    4. (not always) if the video is vertical, rotate it.
    5. run the transcode with ffmpeg
    7. update the transcode job status = COMPLETE
    6. upload the resulting webm file to s3 bucket/others
    """
    logger.info('Started transcode job %s', transcode_job)
    profile = transcoder_profiles.get_profile(transcode_job.profile)
    try:
        metadata = _get_metadata(source_file_path)
    except LookupError:
        logger.warning(
            'Failed to get metadata %s', transcode_job, exc_info=True
        )
        _mark_failed(transcode_job)
        return None
    if profile.height > metadata['height']:
        logger.warning(
            'Failed profile height check %s. Investigate.',
            transcode_job,
            exc_info=True
        )
        _mark_completed(transcode_job)
        return None
    if not (
        profile.min_framerate <= metadata['framerate'] <= profile.max_framerate
    ):
        logger.warning(
            'Failed profile framerate check %s. Investigate.',
            transcode_job,
            exc_info=True
        )
        _mark_completed(transcode_job)
        return None

    tmp_dir = tempfile.mkdtemp()
    output_file_path = Path(tmp_dir) / profile.storage_filename
    try:
        output_file_path, thumbnails = _ffmpeg_transcode_video(
            source_file_path=source_file_path,
            profile=profile,
            output_file_path=output_file_path,
        )
    except RuntimeError:
        logger.warning(
            'FFMPEG transcode unexpectedly failed, %s',
            transcode_job,
            exc_info=True
        )
        _mark_failed(transcode_job)
        return None
    else:
        logger.info('FFMPEF transcode done')
        metadata_transcoded = _get_metadata(output_file_path)
        logger.info(
            'Persisting transcoded video %s %s...', transcode_job,
            transcode_job.video.id
        )
        media_file = _persist_media_file(
            video_record=transcode_job.video,
            video_path=output_file_path,
            metadata=metadata_transcoded,
            profile=profile,
        )
        logger.info(
            'Persisting thumbnails %s %s...', transcode_job,
            transcode_job.video.id
        )
        _persist_media_file_thumbs(
            media_file_record=media_file, thumbnails=thumbnails
        )
        _mark_completed(transcode_job)
        # TODO: cleanup TMP files
        logger.info('Completed transcode job %s', transcode_job)
        return output_file_path, thumbnails


def _get_metadata(video_path):
    metadata = FFProbe(str(video_path))
    try:
        first_stream = metadata.video[0]
    except IndexError as exc:
        raise LookupError('Could not get metadata') from exc

    audio_codec = None
    if metadata.audio:
        audio_stream = metadata.audio[0]
        audio_codec = audio_stream.codec_name

    if first_stream.duration.upper() == 'N/A':
        duration_str = first_stream.__dict__['TAG:DURATION'].split('.')[0]
        struct_time = time.strptime(duration_str, '%H:%M:%S')
        hours = struct_time.tm_hour * 3600
        mins = struct_time.tm_min * 60
        seconds = struct_time.tm_sec
        duration_secs = hours + mins + seconds
    else:
        duration_secs = first_stream.duration_seconds()
    return {
        'width': int(first_stream.width),
        'height': int(first_stream.height),
        'framerate': int(first_stream.framerate),
        'duration': duration_secs,
        'video_codec': first_stream.codec_name,
        'audio_codec': audio_codec,
        'file_size': video_path.stat().st_size,
    }


def _get_thumbnail_time_offsets(video_path):
    """
    Returns time offsets for generating thumbnails across a whole video.

    https://superuser.com/a/821680/1180593
    """
    metadata = _get_metadata(video_path=video_path)
    one_every_secs = 30
    num_thumbnails = int(max(1, metadata['duration'] / one_every_secs))
    offsets = []
    for idx in range(num_thumbnails):
        thumb_num = idx + 1
        time_offset = int(
            (thumb_num - 0.5) * metadata['duration'] / num_thumbnails
        )
        offsets.append(time_offset)
    return tuple(offsets)


def _ffmpeg_generate_thumbnails(*, video_file_path):
    """
    Generate a thumbnail image for every 30 secs of video.
    """
    time_offsets = _get_thumbnail_time_offsets(video_path=video_file_path)
    thumbnails = []
    for offset in time_offsets:
        thumb_path = video_file_path.parent / f'{offset}.jpg'
        command = (
            'ffmpeg '
            f'-ss {offset} '
            f'-i {video_file_path} '
            '-vf "select=gt(scene\,0.4)" '  # noqa: W605
            '-vf select="eq(pict_type\,I)" '  # noqa: W605
            '-vframes 1 '
            f'{thumb_path}'
        )
        result = os.system(command)
        if result != 0:
            raise RuntimeError('Thumbnail creation failed')
        if not thumb_path.exists():
            raise RuntimeError('No file output from transcode thumb process')
        thumbnails.append((offset, thumb_path))
    return tuple(thumbnails)


def _ffmpeg_transcode_video(*, source_file_path, profile, output_file_path):
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
    if not output_file_path.exists():
        # TODO: test
        raise RuntimeError('No file output from transcode process')

    thumbnails = _ffmpeg_generate_thumbnails(video_file_path=output_file_path)
    return output_file_path, tuple(thumbnails)


def _persist_media_file(*, video_record, video_path, metadata, profile):
    with video_path.open('rb') as file_:
        return models.MediaFile.objects.create(
            video=video_record,
            file=File(file_),
            name=profile.name,
            width=metadata['width'],
            height=metadata['height'],
            duration=metadata['duration'],
            ext=video_path.suffix.replace('.', ''),
            framerate=metadata['framerate'],
            audio_codec=metadata['audio_codec'],
            video_codec=metadata['video_codec'],
            file_size=metadata['file_size'],
            # TODO: fill
            container=None,
        )


def _persist_media_file_thumbs(*, media_file_record, thumbnails):
    for time_offset_secs, thumb_path in thumbnails:
        with thumb_path.open('rb') as file_:
            models.MediaFileThumbnail.objects.create(
                media_file=media_file_record,
                file=File(file_),
                ext=thumb_path.suffix.replace('.', ''),
                # TODO: fill
                width=0,
                height=0,
            )


def _mark_completed(transcode_job):
    transcode_job.status = 'completed'
    transcode_job.ended_on = timezone.now()


def _mark_failed(transcode_job):
    transcode_job.status = 'failed'
    transcode_job.ended_on = timezone.now()
