from rest_framework import serializers

from . import models
from . import services


class ChannelSerializer(serializers.ModelSerializer):
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
        )

    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)
        is_selected = validated_data.get('is_selected', instance.is_selected)
        description = validated_data.get(
            'description', instance.description
        )
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


class ChannelAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Channel
        fields = (
            'avatar_image_small_url',
            'avatar_image_large_url',
        )


class ChannelBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Channel
        fields = (
            'banner_image_large_url',
        )
