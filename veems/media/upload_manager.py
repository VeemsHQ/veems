from . import models


def _get_presigned_upload_url():
    return 'https://example.com'


def prepare():
    # TODO: create upload
    upload = models.Upload.objects.create(
        media_type='video', presigned_upload_url=_get_presigned_upload_url(),
    )
    video = models.Video.objects.create(upload=upload)
    return upload, video


def complete(upload_id):
    # transcode_manager.create_transcodes(upload_id)
    pass
