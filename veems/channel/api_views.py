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
