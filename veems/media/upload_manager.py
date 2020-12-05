from . import models
from .video.transcoder import manager as transcode_manager


def _get_presigned_upload_url():
    # TODO: get this from storage provider
    return 'https://example.com'


def prepare():
    upload = models.Upload.objects.create(
        media_type='video',
        presigned_upload_url=_get_presigned_upload_url(),
    )
    video = models.Video.objects.create(upload=upload)
    return upload, video


def complete(upload_id):
    video_id = models.Video.objects.get(upload_id=upload_id).id
    transcode_manager.create_transcodes(video_id=video_id)
