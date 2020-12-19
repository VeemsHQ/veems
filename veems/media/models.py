from pathlib import Path
from django.db import models
from django.contrib.postgres.fields import ArrayField

from ..common.models import BaseModel
from . import storage_backends

TRANSCODE_JOB_CHOICES = (
    'created',
    'processing',
    'completed',
    'failed',
)

VIDEO_VISIBILITY_CHOICES = (
    'private',
    'public',
    'unlisted',
)


def _upload_file_upload_to(instance, filename):
    return f'{instance.id}{Path(filename).suffix}'


def _mediafile_upload_to(instance, filename):
    return f'{instance.id}{Path(filename).suffix}'


def _mediafile_hls_playlist_file_upload_to(instance, filename):
    return f'manifests/{instance.id}_{instance.name}.m3u8'


def _mediafile_segment_upload_to(instance, filename):
    # TODO: test
    return f'{instance.media_file.id}/{instance.segment_number}.ts'


def _media_file_thumbnail_upload_to(instance, filename):
    return f'{instance.media_file.id}/{instance.id}{Path(filename).suffix}'


class Upload(BaseModel):
    presigned_upload_url = models.URLField()
    media_type = models.CharField(max_length=200)
    file = models.FileField(
        upload_to=_upload_file_upload_to,
        storage=storage_backends.UploadStorage
    )


class Video(BaseModel):
    upload = models.OneToOneField(Upload, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    visibility = models.CharField(
        max_length=10,
        choices=tuple((c, c) for c in VIDEO_VISIBILITY_CHOICES),
    )
    description = models.TextField(max_length=5000)
    tags = ArrayField(models.CharField(max_length=1000), null=True)
    # master HLS playlist
    """
    #EXTM3U
    #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=670000,RESOLUTION=640x286,CODECS="mp4a.40.2,avc1.77.30",CLOSED-CAPTIONS=NONE
    https://videos-fms.jwpsrv.com/0_5fdbe624_0xbcae7ced86220f87ab1d5871235f7a648847e373/content/conversions/zWLy8Jer/videos/21ETjILN-1753142.mp4.m3u8
    #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=3400000,RESOLUTION=1920x858,CODECS="mp4a.40.2,avc1.77.30",CLOSED-CAPTIONS=NONE
    https://videos-fms.jwpsrv.com/0_5fdbe624_0xc58d58eef40e11e0c3b4b9643a181efb7d82fd93/content/conversions/zWLy8Jer/videos/21ETjILN-1703854.mp4.m3u8
    #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1710000,RESOLUTION=1280x572,CODECS="mp4a.40.2,avc1.77.30",CLOSED-CAPTIONS=NONE
    https://videos-fms.jwpsrv.com/0_5fdbe624_0x78b5d73f8a1012b57d136b6483274a2217b83375/content/conversions/zWLy8Jer/videos/21ETjILN-364768.mp4.m3u8
    #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=380000,RESOLUTION=320x142,CODECS="mp4a.40.2,avc1.77.30",CLOSED-CAPTIONS=NONE
    https://videos-fms.jwpsrv.com/0_5fdbe624_0x98555078c0222c204484a351db7c340ea098f5ac/content/conversions/zWLy8Jer/videos/21ETjILN-364765.mp4.m3u8
    #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=120000,CODECS="mp4a.40.2"
    https://videos-fms.jwpsrv.com/0_5fdbe624_0x74ab8d285779fd68fe82bad669460deca8e00000/content/conversions/zWLy8Jer/videos/21ETjILN-588477.m4a.m3u8
    """


class MediaFile(BaseModel):
    """
    A format/rendition to be linked to a Video.

    Either a piece of Audio/Video/Audio+Video.
    """
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=_mediafile_upload_to,
        storage=storage_backends.MediaFileStorage
    )
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    framerate = models.IntegerField(null=True)
    duration = models.IntegerField(null=True)
    name = models.CharField(max_length=30, null=False)
    ext = models.CharField(max_length=4, null=False)
    audio_codec = models.CharField(max_length=50, null=True)
    video_codec = models.CharField(max_length=50, null=True)
    container = models.CharField(max_length=30, null=True)
    codecs_string = models.CharField(max_length=100, null=True)
    file_size = models.IntegerField()
    metadata = models.JSONField(null=True)
    hls_playlist_file = models.FileField(
        upload_to=_mediafile_hls_playlist_file_upload_to,
        storage=storage_backends.MediaFileStorage
    )


class MediaFileSegment(BaseModel):
    media_file = models.ForeignKey(MediaFile, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=_mediafile_segment_upload_to,
        storage=storage_backends.MediaFileStorage
    )
    segment_number = models.IntegerField()

    class Meta:
        unique_together = ('media_file', 'segment_number')


class MediaFileThumbnail(BaseModel):
    media_file = models.ForeignKey(MediaFile, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=_media_file_thumbnail_upload_to,
        storage=storage_backends.MediaFileThumbnailStorage
    )
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    time_offset_secs = models.IntegerField(null=True)
    ext = models.CharField(max_length=4, null=False)


class TranscodeJob(BaseModel):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)
    profile = models.CharField(max_length=100)
    executor = models.CharField(max_length=20)
    status = models.CharField(
        max_length=10, choices=tuple((c, c) for c in TRANSCODE_JOB_CHOICES)
    )
    started_on = models.DateTimeField(db_index=True, null=True)
    ended_on = models.DateTimeField(db_index=True, null=True)
    failure_context = models.TextField(null=True)

    def __str__(self):
        return (
            f'<{self.__class__.__name__} {self.id} '
            f'{self.profile} {self.status}>'
        )
