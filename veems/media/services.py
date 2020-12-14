import time

from django.utils import timezone
from django.core.files import File
from ffprobe import FFProbe

from . import models


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
            container=video_path.suffix.replace('.', ''),
        )


def persist_media_file_thumbs(*, media_file_record, thumbnails):
    records = []
    for time_offset_secs, thumb_path in thumbnails:
        img_meta = get_metadata(thumb_path)
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


def _ffprobe_get_streams(file_path):
    command = (
        'ffprobe -v quiet -print_format json -show_format -show_streams '
        f'{file_path}'
    )
    result = subprocess.run(command.split(), capture_output=True)
    if result.returncode == 0 and file_path.exists():
        import ipdb; ipdb.set_trace()
    pass


def get_metadata(video_path):
    streams = _ffprobe_get_streams(video_path)
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
    video_bit_rate = int(video_path.stat().st_size / duration_secs)
    return {
        'width': int(first_stream.width),
        'height': int(first_stream.height),
        'framerate': int(first_stream.framerate),
        'duration': duration_secs,
        'video_codec': first_stream.codec_name,
        'audio_codec': audio_codec,
        'file_size': video_path.stat().st_size,
        'video_aspect_ratio': first_stream.display_aspect_ratio,
        'video_bit_rate': video_bit_rate,
    }
