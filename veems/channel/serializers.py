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
        )

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.sync_videos_interested = validated_data.get(
            'sync_videos_interested', instance.sync_videos_interested
        )
        instance.language = validated_data.get('language', instance.language)
        instance.save()
        return instance

    def create(self, validated_data):
        instance = services.create_channel(**validated_data)
        return instance


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
