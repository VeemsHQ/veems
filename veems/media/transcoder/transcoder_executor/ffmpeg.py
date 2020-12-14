import tempfile
import subprocess
import logging
from pathlib import Path

from .. import transcoder_profiles
from ... import services
from .exceptions import TranscodeException

logger = logging.getLogger(__name__)


def transcode(*, transcode_job, source_file_path):
    logger.info('Started transcode job %s', transcode_job)
    profile = transcoder_profiles.get_profile(transcode_job.profile)
    try:
        metadata = services.get_metadata(source_file_path)
    except LookupError:
        logger.warning(
            'Failed to get metadata %s', transcode_job, exc_info=True
        )
        services.mark_transcode_job_failed(transcode_job=transcode_job)
        return None
    # TODO: correct this res check
    # if (
    #     (profile.height * profile.width) <
    #     (metadata['height'] * metadata['width'])
    # ):
    #     logger.warning(
    #         'Failed profile height check %s. Investigate.',
    #         transcode_job,
    #         exc_info=True
    #     )
    #     _mark_completed(transcode_job)
    #     return None
    if not (
        profile.min_framerate <= metadata['framerate'] <= profile.max_framerate
    ):
        logger.warning(
            'Failed profile framerate check %s. Investigate.',
            transcode_job,
            exc_info=True
        )
        services.mark_transcode_job_completed(transcode_job=transcode_job)
        return None

    with tempfile.TemporaryDirectory() as tmp_dir:
        output_file_path = Path(tmp_dir) / profile.storage_filename
        try:
            output_file_path, thumbnails = _ffmpeg_transcode_video(
                source_file_path=source_file_path,
                profile=profile,
                output_file_path=output_file_path,
            )
        except TranscodeException as exc:
            logger.warning(
                'FFMPEG transcode unexpectedly failed, %s',
                transcode_job,
                exc_info=True
            )
            services.mark_transcode_job_failed(
                transcode_job=transcode_job, failure_context=exc.stderr
            )
            return None
        else:
            logger.info('FFMPEG transcode done')
            import ipdb; ipdb.set_trace()
            metadata_transcoded = services.get_metadata(output_file_path)
            logger.info(
                'Persisting transcoded video %s %s...', transcode_job,
                transcode_job.video.id
            )
            media_file = services.persist_media_file(
                video_record=transcode_job.video,
                video_path=output_file_path,
                metadata=metadata_transcoded,
                profile=profile,
            )
            logger.info(
                'Persisting thumbnails %s %s...', transcode_job,
                transcode_job.video.id
            )
            thumbnail_records = services.persist_media_file_thumbs(
                media_file_record=media_file, thumbnails=thumbnails
            )
            services.mark_transcode_job_completed(transcode_job=transcode_job)
            logger.info('Completed transcode job %s', transcode_job)
            return media_file, thumbnail_records


def _get_thumbnail_time_offsets(video_path):
    """
    Returns time offsets for generating thumbnails across a whole video.

    https://superuser.com/a/821680/1180593
    """
    metadata = services.get_metadata(video_path=video_path)
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
        result = subprocess.run(command.split(), capture_output=True)
        if result.returncode == 0 and thumb_path.exists():
            thumbnails.append((offset, thumb_path))
        else:
            logger.warning(
                'Thumbnail creation failed, retrying without filters..'
            )
            command_without_filters = (
                'ffmpeg '
                f'-ss {offset} '
                f'-i {video_file_path} '
                '-vframes 1 '
                f'{thumb_path}'
            )
            result = subprocess.run(
                command_without_filters.split(), capture_output=True
            )
            if result.returncode == 0 and thumb_path.exists():
                thumbnails.append((offset, thumb_path))
            else:
                raise TranscodeException('Thumbnail creation failed')
    return tuple(thumbnails)


def _ffmpeg_transcode_video(*, source_file_path, profile, output_file_path):
    meta = services.get_metadata(source_file_path)
    if meta['width'] > meta['height']:
        scale = f'{profile.width}:-2'
    else:
        scale = f'-2:{profile.height}'
    base_command = (
        f'ffmpeg -y -i {source_file_path} -vf '
        f'scale={scale}  '
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
    command_1 = f'{base_command} -pass 1 ' f'{output_file_path}'
    command_2 = f'{base_command} -pass 2 ' f'{output_file_path}'
    result = subprocess.run(command_1.split(), capture_output=True)
    if result.returncode != 0:
        raise TranscodeException(
            'Transcoding failed', stderr=result.stderr.decode()
        )
    result = subprocess.run(command_2.split(), capture_output=True)
    if result.returncode != 0:
        raise TranscodeException(
            'Transcoding failed', stderr=result.stderr.decode()
        )
    if not output_file_path.exists():
        raise TranscodeException('No file output from transcode process')
    thumbnails = _ffmpeg_generate_thumbnails(video_file_path=output_file_path)
    return output_file_path, tuple(thumbnails)
