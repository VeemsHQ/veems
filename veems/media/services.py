import time
import json
import logging
import subprocess
import functools
import operator

import m3u8
from django.utils import timezone
from django.core.files import File

from . import models
from .transcoder import transcoder_profiles

logger = logging.getLogger(__name__)


def _get_rendition_playlists(video_record):
    def get_width(height):
        return [
            p.width for p in transcoder_profiles.PROFILES if p.height == height
        ][0]

    return [
        {
            'width': video_rendition.width,
            'height': video_rendition.height,
            'frame_rate': video_rendition.framerate,
            'name': video_rendition.name,
            'codecs_string': video_rendition.codecs_string,
            'resolution': (
                f'{get_width(video_rendition.height)}x{video_rendition.height}'
            ),
            'playlist_url': video_rendition.playlist_file.url,
            'bandwidth': int(video_rendition.metadata['format']['bit_rate']),
        }
        for video_rendition in video_record.videorendition_set.all()
        if video_rendition.playlist_file
    ]


def generate_master_playlist(video_id):
    logger.info(
        'Generating master playlist for %s',
        video_id,
    )
    video = models.Video.objects.get(id=video_id)
    playlist_data = _get_rendition_playlists(video)
    variant_m3u8 = m3u8.M3U8()
    if not playlist_data:
        return None
    for item in playlist_data:
        base_url, uri = item['playlist_url'].rsplit('/', 1)
        playlist = m3u8.Playlist(
            item['playlist_url'],
            stream_info={
                'bandwidth': item['bandwidth'],
                'resolution': item['resolution'],
                'codecs': item['codecs_string'],
                'program_id': 1,
                'closed_captions': 'NONE',
                'subtitles': 'NONE',
            },
            media=[],
            base_uri=None,
        )
        variant_m3u8.add_playlist(playlist)
    return variant_m3u8.dumps()


def mark_transcode_job_completed(*, transcode_job):
    transcode_job.status = 'completed'
    transcode_job.ended_on = timezone.now()
    transcode_job.save()
    return transcode_job


def mark_video_as_viewable(*, video):
    video.is_viewable = True
    video.save()
    return video


def mark_transcode_job_failed(*, transcode_job, failure_context=None):
    transcode_job.status = 'failed'
    transcode_job.failure_context = failure_context
    transcode_job.ended_on = timezone.now()
    transcode_job.save()
    return transcode_job


def mark_transcode_job_processing(*, transcode_job):
    transcode_job.status = 'processing'
    transcode_job.started_on = timezone.now()
    transcode_job.save()
    return transcode_job


def persist_video_rendition(
    *, video_record, video_path, metadata, profile, codecs_string
):
    metadata_summary = metadata['summary']
    with video_path.open('rb') as file_:
        return models.VideoRendition.objects.create(
            video=video_record,
            file=File(file_),
            name=profile.name,
            width=metadata_summary['width'],
            height=metadata_summary['height'],
            duration=metadata_summary['duration'],
            ext=video_path.suffix.replace('.', ''),
            framerate=metadata_summary['framerate'],
            audio_codec=metadata_summary['audio_codec'],
            video_codec=metadata_summary['video_codec'],
            file_size=metadata_summary['file_size'],
            container=video_path.suffix.replace('.', ''),
            metadata=metadata,
            codecs_string=codecs_string,
        )


def persist_video_rendition_segments(
    *, video_rendition, segments_playlist_file, segments
):
    with segments_playlist_file.open('rb') as file_:
        video_rendition.playlist_file = File(file_)
        video_rendition.save()
    for segment_path in segments:
        with segment_path.open('rb') as file_:
            models.VideoRenditionSegment.objects.create(
                video_rendition=video_rendition,
                file=File(file_),
                segment_number=int(segment_path.stem),
            )


def persist_video_rendition_thumbs(*, video_rendition_record, thumbnails):
    records = []
    for time_offset_secs, thumb_path in thumbnails:
        img_meta = get_metadata(thumb_path)['summary']
        with thumb_path.open('rb') as file_:
            records.append(
                models.VideoRenditionThumbnail.objects.create(
                    video_rendition=video_rendition_record,
                    file=File(file_),
                    ext=thumb_path.suffix.replace('.', ''),
                    time_offset_secs=time_offset_secs,
                    width=img_meta['width'],
                    height=img_meta['height'],
                )
            )
    return records


def _ffprobe(file_path):
    command = (
        'ffprobe -v quiet -print_format json -show_format -show_streams '
        f'{file_path}'
    )
    result = subprocess.run(command.split(), capture_output=True)
    if result.returncode == 0 and file_path.exists():
        return json.loads(result.stdout)
    raise LookupError(
        f'FFProbe failed for {file_path}, output: {result.stderr}'
    )


def get_metadata(video_path):
    probe_data = _ffprobe(video_path)

    video_stream = [
        x for x in probe_data['streams'] if x['codec_type'] == 'video'
    ][0]
    try:
        audio_stream = [
            x for x in probe_data['streams'] if x['codec_type'] == 'audio'
        ][0]
    except IndexError:
        audio_stream = None
    format_ = probe_data['format']

    if video_stream.get('duration') is None:
        try:
            duration_str = video_stream['tags']['DURATION'].split('.')[0]
        except KeyError:
            duration_secs = float(probe_data['format']['duration'])
        else:
            struct_time = time.strptime(duration_str, '%H:%M:%S')
            hours = struct_time.tm_hour * 3600
            mins = struct_time.tm_min * 60
            seconds = struct_time.tm_sec
            duration_secs = float(hours + mins + seconds)
    else:
        duration_secs = float(video_stream['duration'])

    def parse_framerate(framerate_str):
        return functools.reduce(
            operator.truediv, map(int, framerate_str.split('/'))
        )

    try:
        frame_rate = parse_framerate(video_stream['avg_frame_rate'])
    except ZeroDivisionError:
        frame_rate = parse_framerate(video_stream['r_frame_rate'])

    try:
        audio_codec_name = audio_stream['codec_name']
    except TypeError:
        audio_codec_name = None
    summary = {
        'width': int(video_stream['width']),
        'height': int(video_stream['height']),
        'framerate': round(frame_rate),
        'duration': duration_secs,
        'video_codec': video_stream['codec_name'],
        'audio_codec': audio_codec_name,
        'file_size': int(format_['size']),
        'video_aspect_ratio': video_stream.get('display_aspect_ratio'),
        'video_bit_rate': int(format_['bit_rate']),
    }
    return {
        'video_stream': video_stream,
        'audio_stream': audio_stream,
        'format': format_,
        'summary': summary,
    }


def get_video(**kwargs):
    return models.Video.objects.get(**kwargs)


def get_videos(channel_id=None):
    if channel_id:
        return models.Video.objects.filter(channel_id=channel_id)
    return models.Video.objects.all()


def get_popular_videos():
    return models.Video.objects.filter(
        is_viewable=True, visibility='public'
    ).order_by('-created_on')


def create_video(*, upload, **kwargs):
    return models.Video.objects.create(
        upload_id=upload.id,
        channel_id=upload.channel_id,
        **kwargs,
    )


def set_video_default_thumbnail_image(*, video_record, thumbnail_paths):
    logger.info('Setting default thumbnail for video %s...', video_record.id)
    image_path = thumbnail_paths[0]
    image_path = _generate_default_thumbnail_image(image_path=image_path)
    with image_path.open('rb') as file_:
        video_record.default_thumbnail_image = File(file_)
        video_record.save()
    logger.info('Done setting default thumbnail for video %s', video_record.id)
    return video_record


def _generate_default_thumbnail_image(image_path):
    """
    Generates a default thumbnail image.

    If there are black bars around the video due to it being vertical for e.g.
    then those spaces will be filled with expanded blurred video content.
    """
    command = (
        'ffmpeg '
        f'-i {image_path} '
        '-filter_complex [0]scale=hd720,setsar=1,boxblur=15:15[b];'
        '[b]eq=brightness=-0.2[b];'
        '[0]scale=-1:720[v];'
        '[b][v]overlay=(W-w)/2 '
        f'{image_path} -y'
    )
    result = subprocess.run(command.split(), capture_output=True)
    if result.returncode == 0 and image_path.exists():
        return image_path
    else:
        raise RuntimeError(result.stderr)


def set_video_custom_thumbnail_image(*, video_record, thumbnail_image):
    logger.info('Setting custom thumbnail for video %s...', video_record.id)
    video_record.custom_thumbnail_image = thumbnail_image
    video_record.save()
    return video_record
