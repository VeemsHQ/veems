import logging
from pathlib import Path
from http.client import CREATED, BAD_REQUEST, OK, NO_CONTENT

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from . import upload_manager, serializers, models, services


logger = logging.getLogger(__name__)


@api_view(['PUT'])
def upload_prepare(request):
    try:
        filename = request.data['filename']
    except KeyError:
        return Response(
            {'detail': 'Filename not provided'}, status=BAD_REQUEST
        )
    try:
        channel_id = request.data['channel_id']
    except KeyError:
        return Response(
            {'detail': 'channel_id not provided'}, status=BAD_REQUEST
        )
    if not Path(filename).suffix:
        return Response({'detail': 'Filename invalid'}, status=BAD_REQUEST)
    upload, video = upload_manager.prepare(
        user=request.user,
        filename=filename,
        channel_id=channel_id,
    )
    return Response(
        {
            'upload_id': upload.id,
            'presigned_upload_url': upload.presigned_upload_url,
            'video_id': video.id,
        },
        status=CREATED,
    )


@api_view(['PUT'])
def upload_complete(request, upload_id):
    # Verify the auth'd user owns this upload.
    models.Upload.objects.get(id=upload_id, channel__user_id=request.user.id)
    upload_manager.complete.delay(upload_id)
    return Response({}, status=OK)


class VideoDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, video_id, format=None):
        video = models.Video.objects.get(id=video_id)
        data = serializers.VideoSerializer(video).data
        return Response(data, status=OK)

    def put(self, request, video_id, format=None):
        video = models.Video.objects.get(
            id=video_id, channel__user_id=request.user.id
        )
        serializer = serializers.VideoSerializer(
            video, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        video = serializer.save()
        serializer = serializers.VideoSerializer(video)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def video_playlist(request, video_id):
    playlist_str = services.generate_master_playlist(video_id=video_id)
    if not playlist_str:
        return HttpResponse('', status=NO_CONTENT)
    content_type = 'Content-Type: application/vnd.apple.mpegurl'
    return HttpResponse(playlist_str, status=OK, content_type=content_type)
