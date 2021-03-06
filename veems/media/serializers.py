import time
import operator

from cachetools import cachedmethod, LRUCache
from rest_framework import serializers
from django.urls import reverse
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.exceptions import ObjectDoesNotExist

from . import models
from . import services
from ..common.serializers import CustomModelSerializer, DEFAULT_EXCLUDE
from . import thumbnails


def _get_video_likedislike_counts(*, likes, dislikes):
    total = likes + dislikes
    if total == 0:
        return 50.0
    if likes > dislikes:
        percentage = likes / total * 100
    else:
        percentage = dislikes / total * 100
    return float(percentage)


class VideoLikeDislikeSerializer(CustomModelSerializer):
    def __init__(self, *args, **kwargs):
        CustomModelSerializer.__init__(self, *args, **kwargs)
        self.cache = LRUCache(maxsize=1000)

    likes_count = serializers.SerializerMethodField(
        method_name='get_likes_count'
    )
    dislikes_count = serializers.SerializerMethodField(
        method_name='get_dislikes_count'
    )
    likesdislikes_percentage = serializers.SerializerMethodField(
        method_name='get_likesdislikes_percentage'
    )

    @cachedmethod(operator.attrgetter('cache'))
    def _get_video_likedislike_counts(self, video_id):
        return services.get_video_likedislike_count(video_id=video_id)

    def get_likes_count(self, instance):
        counts = self._get_video_likedislike_counts(video_id=instance.video_id)
        return counts['like_count']

    def get_dislikes_count(self, instance):
        counts = self._get_video_likedislike_counts(video_id=instance.video_id)
        return counts['dislike_count']

    @cachedmethod(operator.attrgetter('cache'))
    def get_likesdislikes_percentage(self, instance):
        likes = self.get_likes_count(instance=instance)
        dislikes = self.get_dislikes_count(instance=instance)
        return _get_video_likedislike_counts(likes=likes, dislikes=dislikes)

    class Meta:
        model = models.VideoLikeDislike
        fields = (
            'video_id',
            'is_like',
            'likes_count',
            'dislikes_count',
            'likesdislikes_percentage',
        )
        extra_kwargs = {
            'video_id': {'read_only': True},
            'is_like': {'read_only': True},
            'likes_count': {'read_only': True},
            'dislikes_count': {'read_only': True},
        }


class VideoRenditionThumbnailSerializer(CustomModelSerializer):
    class Meta:
        model = models.VideoRenditionThumbnail
        fields = ['id', 'file']


class UploadSerializer(CustomModelSerializer):
    autogenerated_thumbnail_choices = serializers.SerializerMethodField(
        method_name='get_autogenerated_thumbnail_choices'
    )
    thumbnail_image_small_url = serializers.SerializerMethodField(
        method_name='get_thumbnail_image_small_url'
    )

    def get_thumbnail_image_small_url(self, instance):
        return instance.video.thumbnail_image_small_url

    def get_autogenerated_thumbnail_choices(self, instance):
        thumbs = thumbnails.get_autogenerated_thumbnail_choices(
            video_record=instance.video
        )
        return tuple(
            {
                'id': thumb.id,
                'file': thumb.file.url,
                'height': thumb.height,
                'width': thumb.width,
                'time_offset_secs': thumb.time_offset_secs,
            }
            for thumb in thumbs
        )

    class Meta:
        model = models.Upload
        fields = [
            'id',
            'channel_id',
            'video_id',
            'status',
            'autogenerated_thumbnail_choices',
            'thumbnail_image_small_url',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'channel_id': {'read_only': True},
            'video_id': {'read_only': True},
            'status': {'read_only': True},
            'autogenerated_thumbnail_choices': {'read_only': True},
            'thumbnail_image_small_url': {'read_only': True},
        }


class UploadSummarySerializer(UploadSerializer):
    class Meta:
        model = UploadSerializer.Meta.model
        fields = [
            'id',
            'channel_id',
            'video_id',
            'status',
        ]
        extra_kwargs = UploadSerializer.Meta.extra_kwargs


class VideoRenditionSerializer(CustomModelSerializer):
    rendition_thumbnails = VideoRenditionThumbnailSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = models.VideoRendition
        exclude = ['file'] + DEFAULT_EXCLUDE


class TranscodeJobSerializer(CustomModelSerializer):
    class Meta:
        model = models.TranscodeJob
        exclude = ['failure_context'] + DEFAULT_EXCLUDE


class VideoSerializer(CustomModelSerializer):
    def __init__(self, user_id=None, *args, **kwargs):
        CustomModelSerializer.__init__(self, *args, **kwargs)
        self._user_id = user_id
        self.cache = LRUCache(maxsize=1000)

    video_renditions = VideoRenditionSerializer(
        many=True, read_only=True, source='renditions'
    )
    transcode_jobs = TranscodeJobSerializer(many=True, read_only=True)
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
    likesdislikes_percentage = serializers.SerializerMethodField(
        method_name='get_likesdislikes_percentage'
    )
    authenticated_user_data = serializers.SerializerMethodField(
        method_name='get_authenticated_user_data'
    )
    autogenerated_thumbnail_choices = serializers.SerializerMethodField(
        method_name='get_autogenerated_thumbnail_choices'
    )
    upload = serializers.SerializerMethodField(method_name='get_upload')

    def get_autogenerated_thumbnail_choices(self, instance):
        thumbs = thumbnails.get_autogenerated_thumbnail_choices(
            video_record=instance
        )
        return tuple(
            {
                'id': thumb.id,
                'file': thumb.file.url,
                'height': thumb.height,
                'width': thumb.width,
                'time_offset_secs': thumb.time_offset_secs,
            }
            for thumb in thumbs
        )

    def get_playlist_file(self, instance):
        video_id = instance.id
        url = reverse('api-video-playlist', args=[video_id])
        return url

    def get_video_renditions_count(self, instance):
        return instance.renditions.count()

    def get_created_date(self, instance):
        return instance.created_on.date().isoformat()

    def get_created_date_human(self, instance):
        return instance.created_on.strftime('%d %b %Y')

    def get_upload(self, instance):
        return instance.uploads.first().id

    def get_view_count(self, instance):
        return 0

    def get_comment_count(self, instance):
        return 0

    @cachedmethod(operator.attrgetter('cache'))
    def _get_video_likedislike_counts(self, video_id):
        return services.get_video_likedislike_count(video_id=video_id)

    def get_likes_count(self, instance):
        counts = self._get_video_likedislike_counts(video_id=instance.id)
        return counts['like_count']

    def get_dislikes_count(self, instance):
        counts = self._get_video_likedislike_counts(video_id=instance.id)
        return counts['dislike_count']

    @cachedmethod(operator.attrgetter('cache'))
    def get_likesdislikes_percentage(self, instance):
        likes = self.get_likes_count(instance=instance)
        dislikes = self.get_dislikes_count(instance=instance)
        return _get_video_likedislike_counts(likes=likes, dislikes=dislikes)

    def get_authenticated_user_data(self, instance):
        if self._user_id:
            try:
                has_liked_video = services.get_video_likedislike(
                    video_id=instance.id,
                    user_id=self._user_id,
                ).is_like
            except ObjectDoesNotExist:
                return {'has_liked_video': None}
            return {'has_liked_video': has_liked_video}
        return {}

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
            'filename',
            'visibility',
            'description',
            'is_viewable',
            'autogenerated_thumbnail_choices',
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
            'likesdislikes_percentage',
            'authenticated_user_data',
            'upload',
        ]
        extra_kwargs = {
            'channel': {'read_only': True},
            'is_viewable': {'read_only': True},
            'filename': {'read_only': True},
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
            'autogenerated_thumbnail_choices': {'read_only': True},
        }


class VideoSummarySerializer(VideoSerializer):
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


class UploadPartSerializer(serializers.Serializer):
    etag = serializers.CharField(required=True, min_length=20, max_length=40)
    part_number = serializers.IntegerField(required=True)
