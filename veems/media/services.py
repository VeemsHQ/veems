import time
import json
import logging
import subprocess
import functools
from pathlib import Path
import operator
import tempfile

from django.core.files.base import ContentFile
import m3u8
from imagekit.exceptions import MissingSource
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count
from django.utils import timezone
from django.core.files import File

from . import models
from ..channel import services as channel_services
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
            'profile': video_rendition.profile,
            'codecs_string': video_rendition.codecs_string,
            'resolution': (
                f'{get_width(video_rendition.height)}x{video_rendition.height}'
            ),
            'playlist_url': video_rendition.playlist_file.url,
            'bandwidth': int(video_rendition.metadata['format']['bit_rate']),
        }
        for video_rendition in video_record.renditions.all()
        if video_rendition.playlist_file
    ]


def generate_master_playlist(video_id):
    logger.info(
        'Generating master playlist for %s',
        video_id,
    )
    video = get_video(id=video_id)
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
    transcode_job.save(update_fields=('status', 'ended_on'))
    transcode_job.refresh_from_db()
    return transcode_job


def mark_video_as_viewable(*, video):
    video.is_viewable = True
    video.save(update_fields=('is_viewable',))
    video.refresh_from_db()
    return video


def mark_transcode_job_failed(*, transcode_job, failure_context=None):
    transcode_job.status = 'failed'
    transcode_job.failure_context = failure_context
    transcode_job.ended_on = timezone.now()
    transcode_job.save(
        update_fields=(
            'status',
            'failure_context',
            'ended_on',
        )
    )
    transcode_job.refresh_from_db()
    return transcode_job


def mark_transcode_job_processing(*, transcode_job):
    transcode_job.status = 'processing'
    transcode_job.started_on = timezone.now()
    transcode_job.save(
        update_fields=(
            'status',
            'started_on',
        )
    )
    transcode_job.refresh_from_db()
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
            profile=profile.name,
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
        video_rendition.save(update_fields=('playlist_file',))
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
            try:
                duration_secs = float(probe_data['format']['duration'])
            except KeyError:
                # TODO: test, its img
                duration_secs = None
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
        # TODO: fails on images, make func for images
        'video_bit_rate': int(format_['bit_rate']),
    }
    return {
        'video_stream': video_stream,
        'audio_stream': audio_stream,
        'format': format_,
        'summary': summary,
    }


def get_video(include_deleted=False, **kwargs):
    manager = models.Video.objects
    if include_deleted:
        manager = models.Video.objects_all
    return manager.get(**kwargs)


def delete_video(id):
    logger.info('Deleting video %s...', id)
    video = get_video(include_deleted=True, id=id)
    video.deleted_on = timezone.now()
    video.save(update_fields=('deleted_on',))
    return video


def get_videos(channel_id=None, user_id=None):
    logger.info(
        'Getting videos for channel %s, user %s...', channel_id, user_id
    )
    filters = {}
    only_return_public = True
    if channel_id:
        filters['channel_id'] = channel_id
    if channel_id and user_id:
        try:
            channel_services.get_channel(id=channel_id, user_id=user_id)
        except ObjectDoesNotExist:
            # The auth'd user doesn't own this channel so don't return
            # non-public videos.
            only_return_public = True
        else:
            only_return_public = False
    if only_return_public:
        filters['visibility'] = 'public'
    return models.Video.objects.filter(**filters)


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
        video_record.save(update_fields=('default_thumbnail_image',))
    cached_attrs = (
        'default_thumbnail_image_small',
        'default_thumbnail_image_medium',
        'default_thumbnail_image_large',
    )
    for attr in cached_attrs:
        getattr(video_record, attr).generate(force=True)
    logger.info('Done setting default thumbnail for video %s', video_record.id)
    video_record.refresh_from_db()
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


def _resize_thumbnail_to_exact_profile_size(*, thumbnail_path, profile_name):
    logger.info('Resizing thumbnail to size for profile %s', profile_name)
    profile = transcoder_profiles.get_profile(profile_name)
    command = (
        'ffmpeg '
        f'-i {thumbnail_path} '
        f'-filter_complex [0]scale={profile.width}:{profile.height},'
        'setsar=1,boxblur=15:15[b];[b]eq=brightness=-0.2[b];'
        f'[0]scale=-2:{profile.height}[v];'
        '[b][v]overlay=(W-w)/2 '
        f'{thumbnail_path} '
        '-y '
    )
    result = subprocess.run(command.split(), capture_output=True)
    if result.returncode == 0 and thumbnail_path.exists():
        return Path(thumbnail_path)
    else:
        raise RuntimeError(result.stderr)


def set_video_custom_thumbnail_image_from_rendition_thumbnail(
    *,
    video_record,
    video_rendition_thumbnail_id,
    delete_tempfile=True,
):
    logger.info(
        'Setting custom_thumbnail_image for video %s using rendition thumb %s',
        video_record.id,
        video_rendition_thumbnail_id,
    )
    rendition_thumb = models.VideoRenditionThumbnail.objects.get(
        id=video_rendition_thumbnail_id
    )
    temp_thumb_file = tempfile.NamedTemporaryFile(
        suffix='.jpg', delete=delete_tempfile
    )
    with temp_thumb_file as file_:
        file_.write(rendition_thumb.file.read())
        result_file = _resize_thumbnail_to_exact_profile_size(
            thumbnail_path=Path(temp_thumb_file.name),
            profile_name=rendition_thumb.video_rendition.profile,
        )
        with result_file.open('rb') as rfile_:
            content = ContentFile(rfile_.read())
    video_record = set_video_custom_thumbnail_image(
        video_record=video_record, thumbnail_image=content
    )
    return video_record, result_file


def set_video_custom_thumbnail_image(*, video_record, thumbnail_image):
    logger.info('Setting custom thumbnail for video %s...', video_record.id)
    had_image_before = bool(video_record.custom_thumbnail_image)
    if had_image_before:
        video_record.custom_thumbnail_image.delete()
    # Filename does not matter as it's overwritten by models.py
    # we however need to specify something at this point.
    filename = 'temp.jpg'
    video_record.custom_thumbnail_image.save(filename, thumbnail_image)
    if had_image_before:
        cached_attrs = (
            'custom_thumbnail_image_small',
            'custom_thumbnail_image_medium',
            'custom_thumbnail_image_large',
        )
        for attr in cached_attrs:
            try:
                getattr(video_record, attr).generate(force=True)
            except MissingSource:
                pass
    return video_record


def video_like(*, video_id, user_id):
    record, _ = models.VideoLikeDislike.objects.update_or_create(
        video_id=video_id,
        user_id=user_id,
        defaults={'is_like': True},
    )
    logger.info('Video %s liked by %s', video_id, user_id)
    return record


def video_remove_likedislike(*, video_id, user_id):
    record, _ = models.VideoLikeDislike.objects.update_or_create(
        video_id=video_id,
        user_id=user_id,
        defaults={'is_like': None},
    )
    logger.info('Video %s likedislike removed by %s', video_id, user_id)
    return record


def video_dislike(*, video_id, user_id):
    record, _ = models.VideoLikeDislike.objects.update_or_create(
        video_id=video_id,
        user_id=user_id,
        defaults={'is_like': False},
    )
    logger.info('Video %s disliked by %s', video_id, user_id)
    return record


def get_video_likedislikes(*, video_id):
    return models.VideoLikeDislike.objects.filter(video_id=video_id)


def get_video_likedislike(*, video_id, user_id):
    return models.VideoLikeDislike.objects.get(
        video_id=video_id, user_id=user_id
    )


def get_video_likedislike_count(*, video_id):
    return models.VideoLikeDislike.objects.filter(video_id=video_id).aggregate(
        like_count=Count('id', filter=Q(is_like=True)),
        dislike_count=Count('id', filter=Q(is_like=False)),
    )
