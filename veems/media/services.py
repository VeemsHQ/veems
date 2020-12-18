import time
import json
import subprocess
import functools
import operator

from django.utils import timezone
from django.core.files import File

from . import models


def get_rendition_playlists(video_record):

    # def get_codecs(metadata):
    #     vid_meta = metadata['video_stream']
    #     codec_name = vid_meta['codec_name']
    #     codec_tag_string = vid_meta['codec_tag_string']
    #     profile = vid_meta['profile']
    #     level = vid_meta['level']
    #     video_codecs = '.'.join((
    #         # str(codec_name),
    #         str(codec_tag_string),
    #         str(profile),
    #         str(level),
    #     ))
    #     audio_meta = metadata['audio_stream']
    #     codec_name = audio_meta['codec_name']
    #     codec_tag_string = audio_meta['codec_tag_string']
    #     profile = audio_meta['profile']
    #     try:
    #         level = audio_meta['level']
    #     except:
    #         import ipdb; ipdb.set_trace()
    #     audio_codecs = '.'.join((
    #         str(codec_name),
    #         str(codec_tag_string),
    #         str(profile),
    #         str(level),
    #     ))
    #     return ','.join((video_codec, audio_codec))

    # TODO codecs
    # https://developer.apple.com/documentation/http_live_streaming/example_playlists_for_http_live_streaming/creating_a_master_playlist
    return [
        {
            'width': media_file.width,
            'height': media_file.height,
            'name': media_file.name,
            'resolution': f'{media_file.width}x{media_file.height}',
            'playlist_url': media_file.hls_playlist_file.url,
            'bandwidth': int(media_file.metadata['format']['bit_rate']),
            # 'codec': get_codecs(media_file.metadata),
        } for media_file in video_record.mediafile_set.all()
    ]


def mark_transcode_job_completed(*, transcode_job):
    transcode_job.status = 'completed'
    transcode_job.ended_on = timezone.now()
    transcode_job.save()
    return transcode_job


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


def persist_media_file(*, video_record, video_path, metadata, profile):
    metadata_summary = metadata['summary']
    with video_path.open('rb') as file_:
        return models.MediaFile.objects.create(
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
        )


def persist_media_file_segments(
    *, media_file, segments_playlist_file, segments
):
    with segments_playlist_file.open('rb') as file_:
        media_file.hls_playlist_file = File(file_)
        media_file.save()
    for segment_path in segments:
        with segment_path.open('rb') as file_:
            models.MediaFileSegment.objects.create(
                media_file=media_file,
                file=File(file_),
                segment_number=int(segment_path.stem),
            )


def persist_media_file_thumbs(*, media_file_record, thumbnails):
    records = []
    for time_offset_secs, thumb_path in thumbnails:
        img_meta = get_metadata(thumb_path)['summary']
        with thumb_path.open('rb') as file_:
            records.append(
                models.MediaFileThumbnail.objects.create(
                    media_file=media_file_record,
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
        duration_str = video_stream['tags']['DURATION'].split('.')[0]
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
        framerate = parse_framerate(video_stream['avg_frame_rate'])
    except ZeroDivisionError:
        framerate = parse_framerate(video_stream['r_frame_rate'])

    try:
        audio_codec_name = audio_stream['codec_name']
    except TypeError:
        audio_codec_name = None

    summary = {
        'width': int(video_stream['width']),
        'height': int(video_stream['height']),
        'framerate': round(framerate),
        'duration': duration_secs,
        'video_codec': video_stream['codec_name'],
        'audio_codec': audio_codec_name,
        'file_size': int(format_['size']),
        'video_aspect_ratio': video_stream['display_aspect_ratio'],
        'video_bit_rate': int(format_['bit_rate']),
    }
    return {
        'video_stream': video_stream,
        'audio_stream': audio_stream,
        'format': format_,
        'summary': summary,
    }
