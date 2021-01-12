from rest_framework import serializers
from django.urls import reverse

from . import models
from ..common.serializers import CustomModelSerializer


class VideoRenditionSerializer(CustomModelSerializer):
    class Meta:
        model = models.VideoRendition
        exclude = ['file']


class TranscodeJobSerializer(CustomModelSerializer):
    class Meta:
        model = models.TranscodeJob
        exclude = ['failure_context']


class VideoSerializer(CustomModelSerializer):
    video_renditions = VideoRenditionSerializer(
        many=True, read_only=True, source='videorendition_set'
    )
    transcode_jobs = TranscodeJobSerializer(
        many=True, read_only=True, source='transcodejob_set'
    )
    playlist_file = serializers.SerializerMethodField(
        method_name='get_playlist_file'
    )

    def get_playlist_file(self, instance):
        video_id = instance.id
        url = reverse('api-video-playlist', args=[video_id])
        return url

    class Meta:
        model = models.Video
        fields = [
            'id',
            'channel',
            'title',
            'visibility',
            'description',
            'tags',
            'video_renditions',
            'transcode_jobs',
            'playlist_file',
        ]
        extra_kwargs = {
            'channel': {'read_only': True},
            'upload': {'read_only': True},
            'video_renditions': {'read_only': True},
            'transcode_jobs': {'read_only': True},
            'playlist_file': {'read_only': True},
        }
