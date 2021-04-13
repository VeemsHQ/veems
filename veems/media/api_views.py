import logging
from pathlib import Path
from http.client import CREATED, BAD_REQUEST, OK, NO_CONTENT

from django.http import HttpResponse, Http404
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from . import upload_manager, serializers, services


logger = logging.getLogger(__name__)


@api_view(['PUT'])
def upload_prepare(request):
    try:
        filename = request.data['filename']
    except KeyError:
        return Response(
            {'detail': 'filename not provided'}, status=BAD_REQUEST
        )
    try:
        num_parts = int(request.data['num_parts'])
    except KeyError:
        return Response(
            {'detail': 'num_parts not provided'}, status=BAD_REQUEST
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
        num_parts=num_parts,
    )
    return Response(
        {
            'upload_id': upload.id,
            'presigned_upload_urls': upload.presigned_upload_urls,
            'video_id': video.id,
        },
        status=CREATED,
    )


@api_view(['GET'])
def upload_detail(request, upload_id):
    upload = services.get_upload(
        id=upload_id, channel__user_id=request.user.id
    )
    if upload.video.deleted_on:
        raise Http404('Not found')
    data = serializers.UploadSerializer(instance=upload).data
    return Response(data, status=OK)


@api_view(['PUT'])
def upload_complete(request, upload_id):
    try:
        parts = serializers.UploadPartSerializer(
            instance=request.data['parts'], many=True
        ).data
    except (KeyError, ValueError):
        return Response({'detail': 'parts not provided'}, status=BAD_REQUEST)
    # Verify the auth'd user owns this upload.
    upload = services.get_upload(
        id=upload_id, channel__user_id=request.user.id
    )
    services.set_upload_status(upload=upload, status='uploaded')
    upload_manager.complete.delay(upload_id=upload_id, parts=parts)
    return Response({}, status=OK)


class VideoAPIView(APIView):
    def _raise_missing_params(self):
        raise ValidationError('Missing required parameters')

    def get(self, request, format=None):
        try:
            channel_id = request.GET['channel_id']
        except KeyError:
            self._raise_missing_params()
        else:
            if not channel_id:
                self._raise_missing_params()
        videos = services.get_videos(
            channel_id=channel_id, user_id=request.user.id
        )
        data = serializers.VideoSerializer(instance=videos, many=True).data
        return Response(data, status=OK)


class VideoDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, video_id, format=None):
        video = services.get_video(id=video_id)
        data = serializers.VideoSerializer(instance=video).data
        return Response(data, status=OK)

    def put(self, request, video_id, format=None):
        video = services.get_video(
            id=video_id, channel__user_id=request.user.id
        )
        serializer = serializers.VideoSerializer(
            instance=video, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        video = serializer.save()
        serializer = serializers.VideoSerializer(instance=video)
        return Response(serializer.data)

    def delete(self, request, video_id, format=None):
        services.delete_video(id=video_id)
        return HttpResponse('', status=NO_CONTENT)


class VideoLikeDislikeAPIView(APIView):
    def post(self, request, video_id, format=None):
        if request.data['is_like']:
            record = services.video_like(
                video_id=video_id, user_id=request.user.id
            )
        else:
            record = services.video_dislike(
                video_id=video_id, user_id=request.user.id
            )
        serializer = serializers.VideoLikeDislikeSerializer(record)
        return Response(serializer.data)

    def delete(self, request, video_id, format=None):
        record = services.video_remove_likedislike(
            video_id=video_id, user_id=request.user.id
        )
        serializer = serializers.VideoLikeDislikeSerializer(record)
        return Response(serializer.data)


class VideoThumbnailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, video_id, format=None):
        channel = services.get_video(id=video_id)
        serializer = serializers.VideoThumbnailSerializer(channel)
        return Response(serializer.data)

    def post(self, request, video_id, format=None):
        video = services.get_video(
            id=video_id, channel__user_id=request.user.id
        )
        thumbnail_image = request.data['file']
        video = services.set_video_custom_thumbnail_image(
            video_record=video, thumbnail_image=thumbnail_image
        )
        serializer = serializers.VideoThumbnailSerializer(video)
        return Response(serializer.data)


class VideoThumbnailSelectAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(
        self, request, video_id, video_rendition_thumbnail_id, format=None
    ):
        video = services.get_video(
            id=video_id, channel__user_id=request.user.id
        )
        (
            video,
            _,
        ) = services.set_video_custom_thumbnail_image_from_rendition_thumbnail(
            video_record=video,
            video_rendition_thumbnail_id=video_rendition_thumbnail_id,
        )
        data = serializers.VideoSerializer(instance=video).data
        return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def video_playlist(request, video_id):
    playlist_str = services.generate_master_playlist(video_id=video_id)
    if not playlist_str:
        return HttpResponse('', status=NO_CONTENT)
    content_type = 'Content-Type: application/vnd.apple.mpegurl'
    return HttpResponse(playlist_str, status=OK, content_type=content_type)
