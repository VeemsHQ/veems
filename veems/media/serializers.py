import time

from rest_framework import serializers
from django.urls import reverse
from django.contrib.humanize.templatetags.humanize import (
    naturaltime,
    naturalday,
)

from . import models
from ..common.serializers import CustomModelSerializer, DEFAULT_EXCLUDE


class VideoLikeDislikeSerializer(CustomModelSerializer):
    class Meta:
        model = models.VideoLikeDislike
        fields = ('video_id', 'is_like')
        extra_kwargs = {
            'video_id': {'read_only': True},
            'is_like': {'read_only': True},
        }


class VideoRenditionSerializer(CustomModelSerializer):
    class Meta:
        model = models.VideoRendition
        exclude = ['file'] + DEFAULT_EXCLUDE


class TranscodeJobSerializer(CustomModelSerializer):
    class Meta:
        model = models.TranscodeJob
        exclude = ['failure_context'] + DEFAULT_EXCLUDE


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
    created_date_human = serializers.SerializerMethodField(
        method_name='get_created_date_human'
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
    channel_avatar_image_small_url = serializers.SerializerMethodField(
        method_name='get_channel_avatar_image_small_url'
    )
    likes_count = serializers.SerializerMethodField(
        method_name='get_likes_count'
    )
    dislikes_count = serializers.SerializerMethodField(
        method_name='get_dislikes_count'
    )

    def get_playlist_file(self, instance):
        video_id = instance.id
        url = reverse('api-video-playlist', args=[video_id])
        return url

    def get_video_renditions_count(self, instance):
        return instance.videorendition_set.count()

    def get_created_date(self, instance):
        return instance.created_on.date().isoformat()

    def get_created_date_human(self, instance):
        return instance.created_on.strftime('%d %b %Y')
        return naturalday(instance.created_on.date())

    def get_view_count(self, instance):
        return 0

    def get_comment_count(self, instance):
        return 0

    def get_likes_count(self, instance):
        return 0

    def get_dislikes_count(self, instance):
        return 0

    def get_time_ago_human(self, instance):
        return naturaltime(instance.created_on)

    def get_channel_name(self, instance):
        return instance.channel.name

    def get_channel_id(self, instance):
        return instance.channel_id

    def get_channel_avatar_image_small_url(self, instance):
        return instance.channel.avatar_image_small_url

    def get_duration_human(self, instance):
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
            'created_date_human',
            'view_count',
            'comment_count',
            'thumbnail_image_small_url',
            'thumbnail_image_medium_url',
            'thumbnail_image_large_url',
            'time_ago_human',
            'channel_name',
            'channel_id',
            'duration',
            'duration_human',
            'channel_avatar_image_small_url',
            'likes_count',
            'dislikes_count',
        ]
        extra_kwargs = {
            'channel': {'read_only': True},
            'upload': {'read_only': True},
            'video_renditions': {'read_only': True},
            'transcode_jobs': {'read_only': True},
            'playlist_file': {'read_only': True},
            'video_renditions_count': {'read_only': True},
            'created_date': {'read_only': True},
            'created_date_human': {'read_only': True},
            'view_count': {'read_only': True},
            'comment_count': {'read_only': True},
            'time_ago_human': {'read_only': True},
            'channel_name': {'read_only': True},
            'channel_id': {'read_only': True},
            'duration': {'read_only': True},
            'duration_human': {'read_only': True},
            'thumbnail_image_small_url': {'read_only': True},
            'thumbnail_image_medium_url': {'read_only': True},
            'thumbnail_image_large_url': {'read_only': True},
            'channel_avatar_image_small_url': {'read_only': True},
            'likes_count': {'read_only': True},
            'dislikes_count': {'read_only': True},
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
            'created_date_human',
            'view_count',
            'comment_count',
            'thumbnail_image_small_url',
            'thumbnail_image_medium_url',
            'thumbnail_image_large_url',
            'time_ago_human',
            'channel_name',
            'channel_id',
            'duration',
            'duration_human',
            'channel_avatar_image_small_url',
        ]
        extra_kwargs = VideoSerializer.Meta.extra_kwargs


class VideoThumbnailSerializer(CustomModelSerializer):
    class Meta:
        model = models.Video
        fields = (
            'thumbnail_image_small_url',
            'thumbnail_image_medium_url',
            'thumbnail_image_large_url',
        )
        extra_kwargs = {
            'thumbnail_image_small_url': {'read_only': True},
            'thumbnail_image_medium_url': {'read_only': True},
            'thumbnail_image_large_url': {'read_only': True},
        }
