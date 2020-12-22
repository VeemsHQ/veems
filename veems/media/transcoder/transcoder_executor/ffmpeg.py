import tempfile
import subprocess
import logging
import os
from pathlib import Path

import m3u8

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
    metadata_summary = metadata['summary']
    if not (
        profile.min_framerate <= metadata_summary['framerate'] <=
        profile.max_framerate
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
            metadata_transcoded = services.get_metadata(output_file_path)
            logger.info(
                'Persisting transcoded video %s %s...', transcode_job,
                transcode_job.video_id
            )
            video_rendition = services.persist_video_rendition(
                video_record=transcode_job.video,
                video_path=output_file_path,
                metadata=metadata_transcoded,
                profile=profile,
                codecs_string=None,
            )
            logger.info(
                'Creating segments for video %s %s...', transcode_job,
                transcode_job.video_id
            )
            output_playlist_path, segment_paths, codecs_string = (
                _create_segments_for_video(
                    video_path=output_file_path,
                    profile=profile,
                    tmp_dir=tmp_dir,
                    video_rendition_id=video_rendition.id,
                    video_id=video_rendition.video_id,
                )
            )
            video_rendition.codecs_string = codecs_string
            video_rendition.save()
            logger.info(
                'Persisting transcoded video segments %s %s %s...',
                len(segment_paths), transcode_job, transcode_job.video_id
            )
            services.persist_video_rendition_segments(
                video_rendition=video_rendition,
                segments_playlist_file=output_playlist_path,
                segments=segment_paths,
            )
            logger.info(
                'Persisting thumbnails %s %s...', transcode_job,
                transcode_job.video_id
            )
            thumbnail_records = services.persist_video_rendition_thumbs(
                video_rendition_record=video_rendition, thumbnails=thumbnails
            )
            services.mark_transcode_job_completed(transcode_job=transcode_job)
            logger.info('Completed transcode job %s', transcode_job)
            return video_rendition, thumbnail_records


def _create_segments_for_video(
    *, video_path, profile, tmp_dir, video_rendition_id, video_id
):
    output_playlist_path = Path(tmp_dir) / 'rendition.m3u8'
    segments_dir = Path(tmp_dir)
    playlist_ts_prefix = (
        f'/videos/{video_id}/renditions/{video_rendition_id}/segments/'
    )
    segment_filename_pattern = (str(segments_dir) + '/%d.ts')
    tmp_master_file = 'master.m3u8'
    command = (
        'ffmpeg '
        f'-i {video_path} '
        f'-hls_time {profile.segment_duration} '
        f'-hls_segment_filename {segment_filename_pattern} '
        f'-master_pl_name {tmp_master_file} '
        '-hls_playlist_type vod '
        f'{output_playlist_path}'
    )
    result = subprocess.run(command.split(), capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f'Failed to create segments: {result.stderr}')
    segment_paths = tuple(
        sorted(segments_dir.glob('*.ts'), key=os.path.getmtime)
    )
    master_file = tuple(segments_dir.glob(tmp_master_file))[0]
    try:
        codecs_string = (
            m3u8.load(str(master_file)
                      ).data['playlists'][0]['stream_info']['codecs']
        )
    except IndexError:
        codecs_string = None
    with output_playlist_path.open('r') as file_:
        playlist_lines = file_.readlines()
    new_lines = []
    for line in playlist_lines:
        if '.ts' in line:
            line = f'{playlist_ts_prefix}{line}'
            new_lines.append(line)
        else:
            new_lines.append(line)
    new_playlist_file_content = ''.join(new_lines)
    with output_playlist_path.open('w') as file_:
        file_.write(new_playlist_file_content)
    return output_playlist_path, segment_paths, codecs_string


def _get_thumbnail_time_offsets(video_path):
    """
    Returns time offsets for generating thumbnails across a whole video.

    https://superuser.com/a/821680/1180593
    """
    metadata = services.get_metadata(video_path=video_path)
    metadata_summary = metadata['summary']
    one_every_secs = 30
    num_thumbnails = int(max(1, metadata_summary['duration'] / one_every_secs))
    offsets = []
    for idx in range(num_thumbnails):
        thumb_num = idx + 1
        time_offset = int(
            (thumb_num - 0.5) * metadata_summary['duration'] / num_thumbnails
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
        logger.error('Transcoding failed: %s', result.stderr.decode())
        raise TranscodeException(
            'Transcoding failed', stderr=result.stderr.decode()
        )
    result = subprocess.run(command_2.split(), capture_output=True)
    if result.returncode != 0:
        logger.error('Transcoding failed: %s', result.stderr.decode())
        raise TranscodeException(
            'Transcoding failed', stderr=result.stderr.decode()
        )
    if not output_file_path.exists():
        raise TranscodeException('No file output from transcode process')
    thumbnails = _ffmpeg_generate_thumbnails(video_file_path=output_file_path)
    return output_file_path, tuple(thumbnails)
