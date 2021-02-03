from rest_framework import serializers

from . import models
from . import services
from ..media import services as media_services
from ..common.serializers import CustomModelSerializer
from ..media.serializers import VideoSerializer


class ChannelSerializer(CustomModelSerializer):
    followers_count = serializers.SerializerMethodField(
        method_name='get_followers_count'
    )
    created_date = serializers.SerializerMethodField(
        method_name='get_created_date'
    )
    has_banner = serializers.SerializerMethodField(
        method_name='get_has_banner'
    )
    videos_count = serializers.SerializerMethodField(
        method_name='get_videos_count'
    )
    videos = serializers.SerializerMethodField(method_name='get_videos')

    def __init__(self, *, user_id=None, **kwargs):
        CustomModelSerializer.__init__(self, **kwargs)
        self._user_id = user_id

    def get_videos_count(self, instance):
        return self._get_videos(instance=instance).count()

    def _get_videos(self, instance):
        return media_services.get_videos(
            channel_id=instance.id, user_id=self._user_id
        )

    def get_videos(self, instance):
        instance = self._get_videos(instance=instance)
        return VideoSerializer(many=True, instance=instance).data

    def get_followers_count(self, instance):
        return 0

    def get_has_banner(self, instance):
        return bool(instance.banner_image)

    class Meta:
        model = models.Channel
        fields = (
            'id',
            'user',
            'name',
            'description',
            'sync_videos_interested',
            'language',
            'created_on',
            'modified_on',
            'is_selected',
            'videos',
            'followers_count',
            'avatar_image_small_url',
            'avatar_image_large_url',
            'banner_image_small_url',
            'banner_image_large_url',
            'created_date',
            'has_banner',
            'videos_count',
        )
        extra_kwargs = {
            'followers_count': {'read_only': True},
            'avatar_image_small_url': {'read_only': True},
            'avatar_image_large_url': {'read_only': True},
            'banner_image_small_url': {'read_only': True},
            'banner_image_large_url': {'read_only': True},
            'created_date': {'read_only': True},
            'has_banner': {'read_only': True},
            'videos_count': {'read_only': True},
        }

    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)
        is_selected = validated_data.get('is_selected', instance.is_selected)
        description = validated_data.get('description', instance.description)
        sync_videos_interested = validated_data.get(
            'sync_videos_interested', instance.sync_videos_interested
        )
        language = validated_data.get('language', instance.language)
        # TODO: don't allow selecting another user's channel
        return services.update_channel(
            channel=instance,
            language=language,
            is_selected=is_selected,
            sync_videos_interested=sync_videos_interested,
            description=description,
            name=name,
        )

    def create(self, validated_data):
        return services.create_channel(**validated_data)

    def get_created_date(self, instance):
        return instance.created_on.date().isoformat()


class ChannelSlimSerializer(ChannelSerializer):
    class Meta:
        model = models.Channel
        fields = (
            'id',
            'user',
            'name',
            'description',
            'sync_videos_interested',
            'language',
            'created_on',
            'modified_on',
            'is_selected',
            'followers_count',
            'avatar_image_small_url',
            'avatar_image_large_url',
            'banner_image_small_url',
            'banner_image_large_url',
            'created_date',
            'has_banner',
            'videos_count',
        )
        extra_kwargs = {
            'followers_count': {'read_only': True},
            'avatar_image_small_url': {'read_only': True},
            'avatar_image_large_url': {'read_only': True},
            'banner_image_small_url': {'read_only': True},
            'banner_image_large_url': {'read_only': True},
            'created_date': {'read_only': True},
            'has_banner': {'read_only': True},
            'videos_count': {'read_only': True},
        }


class ChannelAvatarSerializer(CustomModelSerializer):
    class Meta:
        model = models.Channel
        fields = (
            'avatar_image_small_url',
            'avatar_image_large_url',
        )
        extra_kwargs = {
            'avatar_image_small_url': {'read_only': True},
            'avatar_image_large_url': {'read_only': True},
        }


class ChannelBannerSerializer(CustomModelSerializer):
    class Meta:
        model = models.Channel
        fields = ('banner_image_large_url',)
        extra_kwargs = {
            'banner_image_large_url': {'read_only': True},
        }
