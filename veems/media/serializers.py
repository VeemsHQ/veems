from rest_framework import serializers

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

    class Meta:
        model = models.Video
        fields = [
            'title', 'visibility', 'description', 'tags', 'media_files',
            'transcode_jobs', 'playlist_file',
        ]
