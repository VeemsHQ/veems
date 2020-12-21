from rest_framework import serializers
from django.urls import reverse

from . import models


class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MediaFile
        exclude = ['file']


class TranscodeJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TranscodeJob
        exclude = ['failure_context']


class VideoSerializer(serializers.ModelSerializer):
    media_files = MediaFileSerializer(
        many=True, read_only=True, source='mediafile_set'
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
            'title',
            'visibility',
            'description',
            'tags',
            'media_files',
            'transcode_jobs',
            'playlist_file',
        ]
