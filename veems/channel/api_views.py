from http.client import BAD_REQUEST, CREATED

from rest_framework.views import APIView
from rest_framework.response import Response

from . import services, serializers


class ChannelAPIView(APIView):
    def get(self, request, format=None):
        channels = services.get_channels(user_id=request.user.id)
        serializer = serializers.ChannelSerializer(channels, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.data['user'] = request.user.id
        serializer = serializers.ChannelSerializer(data=request.data)
        if serializer.is_valid():
            channel = serializer.save()
            serializer = serializers.ChannelSerializer(channel)
            return Response(serializer.data, status=CREATED)
        else:
            return Response({'detail': 'Invalid payload'}, status=BAD_REQUEST)


class ChannelDetailAPIView(APIView):
    def get(self, request, channel_id, format=None):
        channel = services.get_channel(id=channel_id)
        serializer = serializers.ChannelSerializer(channel)
        return Response(serializer.data)

    def put(self, request, channel_id, format=None):
        channel = services.get_channel(id=channel_id, user_id=request.user.id)
        serializer = serializers.ChannelSerializer(
            channel, data=request.data, partial=True
        )
        if serializer.is_valid():
            channel = serializer.save()
            serializer = serializers.ChannelSerializer(channel)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Invalid payload'}, status=BAD_REQUEST)


class ChannelAvatarAPIView(APIView):
    def get(self, request, channel_id, format=None):
        channel = services.get_channel(id=channel_id)
        serializer = serializers.ChannelAvatarSerializer(channel)
        return Response(serializer.data)

    def post(self, request, channel_id, format=None):
        channel = services.get_channel(id=channel_id, user_id=request.user.id)
        avatar_image = request.data['file']
        channel = services.set_channel_avatar_image(
            channel=channel, avatar_image=avatar_image
        )
        serializer = serializers.ChannelAvatarSerializer(channel)
        return Response(serializer.data)


class ChannelBannerAPIView(APIView):
    def get(self, request, channel_id, format=None):
        channel = services.get_channel(id=channel_id)
        serializer = serializers.ChannelBannerSerializer(channel)
        return Response(serializer.data)

    def post(self, request, channel_id, format=None):
        channel = services.get_channel(id=channel_id, user_id=request.user.id)
        banner_image = request.data['file']
        channel = services.set_channel_banner_image(
            channel=channel, banner_image=banner_image
        )
        serializer = serializers.ChannelBannerSerializer(channel)
        return Response(serializer.data)
