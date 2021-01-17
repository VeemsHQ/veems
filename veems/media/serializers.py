import time

from rest_framework import serializers
from django.urls import reverse
from django.contrib.humanize.templatetags.humanize import naturaltime

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
    video_renditions_count = serializers.SerializerMethodField(
        method_name='get_video_renditions_count'
    )
    created_date = serializers.SerializerMethodField(
        method_name='get_created_date'
    )
    view_count = serializers.SerializerMethodField(
        method_name='get_view_count'
    )
    comment_count = serializers.SerializerMethodField(
        method_name='get_comment_count'
    )
    time_ago_human = serializers.SerializerMethodField(
        method_name='get_time_ago_human'
    )
    channel_name = serializers.SerializerMethodField(
        method_name='get_channel_name'
    )
    channel_id = serializers.SerializerMethodField(
        method_name='get_channel_id'
    )
    duration_human = serializers.SerializerMethodField(
        method_name='get_duration_human'
    )

    def get_playlist_file(self, instance):
        video_id = instance.id
        url = reverse('api-video-playlist', args=[video_id])
        return url

    def get_video_renditions_count(self, instance):
        return instance.videorendition_set.count()

    def get_created_date(self, instance):
        return instance.created_on.date()

    def get_view_count(self, instance):
        return 0

    def get_comment_count(self, instance):
        return 0

    def get_time_ago_human(self, instance):
        return naturaltime(instance.created_on)

    def get_channel_name(self, instance):
        return instance.channel.name

    def get_channel_id(self, instance):
        return instance.channel_id

    def get_duration_human(self, instance):
        assert instance.duration is not None
        return time.strftime(
            '%H:%M:%S', time.gmtime(instance.duration)
        ).removeprefix('00:')

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
            'video_renditions_count',
            'created_date',
            'view_count',
            'comment_count',
            'default_thumbnail_image_small_url',
            'time_ago_human',
            'channel_name',
            'channel_id',
            'duration',
            'duration_human',
        ]
        extra_kwargs = {
            'channel': {'read_only': True},
            'upload': {'read_only': True},
            'video_renditions': {'read_only': True},
            'transcode_jobs': {'read_only': True},
            'playlist_file': {'read_only': True},
            'video_renditions_count': {'read_only': True},
            'created_date': {'read_only': True},
            'view_count': {'read_only': True},
            'comment_count': {'read_only': True},
            'time_ago_human': {'read_only': True},
            'channel_name': {'read_only': True},
            'channel_id': {'read_only': True},
            'duration': {'read_only': True},
            'duration_human': {'read_only': True},
            'default_thumbnail_image_small_url': {'read_only': True},
        }


class VideoSlimSerializer(VideoSerializer):
    class Meta:
        model = VideoSerializer.Meta.model
        fields = [
            'id',
            'channel',
            'title',
            'visibility',
            'description',
            'tags',
            'video_renditions_count',
            'created_date',
            'view_count',
            'comment_count',
            'default_thumbnail_image_small_url',
            'time_ago_human',
            'channel_name',
            'channel_id',
            'duration',
            'duration_human',
        ]
        extra_kwargs = VideoSerializer.Meta.extra_kwargs
