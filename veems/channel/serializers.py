from rest_framework import serializers

from . import models
from . import services
from ..common.serializers import CustomModelSerializer
from ..media.serializers import VideoSerializer


class ChannelSerializer(CustomModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)
    followers_count = serializers.SerializerMethodField(
        method_name='get_followers_count'
    )

    def get_followers_count(self, instance):
        return 0

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
            'banner_image_small_url',
        )
        extra_kwargs = {
            'followers_count': {'read_only': True},
            'avatar_image_small_url': {'read_only': True},
            'banner_image_small_url': {'read_only': True},
        }

    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)
        is_selected = validated_data.get('is_selected', instance.is_selected)
        description = validated_data.get('description', instance.description)
        sync_videos_interested = validated_data.get(
            'sync_videos_interested', instance.sync_videos_interested
        )
        language = validated_data.get('language', instance.language)
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
            'banner_image_small_url',
        )
        extra_kwargs = {
            'followers_count': {'read_only': True},
            'avatar_image_small_url': {'read_only': True},
            'banner_image_small_url': {'read_only': True},
        }


class ChannelAvatarSerializer(CustomModelSerializer):
    class Meta:
        model = models.Channel
        fields = (
            'avatar_image_small_url',
            'avatar_image_large_url',
        )


class ChannelBannerSerializer(CustomModelSerializer):
    class Meta:
        model = models.Channel
        fields = ('banner_image_large_url',)
