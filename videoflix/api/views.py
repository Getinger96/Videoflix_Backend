from rest_framework.views import APIView
from .serializers import VideoSerializer
from videoflix.models import Video
from rest_framework.response import Response
from django.http import FileResponse, Http404
import os
from django.conf import settings
from rest_framework.permissions import IsAuthenticated




class VideoListView(APIView):
    """
    API view for listing all available videos.

    Only authenticated users are allowed to access this endpoint.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve and return a list of all videos.

        :param request: HTTP request
        :return: Serialized list of videos
        """
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)


class VideoSegmentView(APIView):
    """
    API view for streaming individual HLS video segments (.ts files).

    The view dynamically builds the file path based on:
    - video ID
    - resolution
    - segment filename
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, resolution, segment):
        """
        Stream a single HLS video segment.

        :param movie_id: ID of the video
        :param resolution: Video resolution (e.g. 720p, 1080p)
        :param segment: Segment filename (e.g. segment_000.ts)
        :return: TS video segment as a streaming response
        :raises Http404: If the video or segment does not exist
        """
        # Validate video existence
        try:
            video = Video.objects.get(pk=movie_id)
        except Video.DoesNotExist:
            raise Http404("Video not found")

        # Build the file system path to the segment
        segment_path = os.path.join(
            settings.MEDIA_ROOT,
            "hls",
            str(movie_id),
            resolution,
            segment
        )

        # Check if the segment file exists
        if not os.path.exists(segment_path):
            raise Http404("Segment not found")

        # Stream the TS segment file
        return FileResponse(
            open(segment_path, "rb"),
            content_type="video/MP2T"
        )


class VideoResolutionPlaylistView(APIView):
    """
    API view for serving the HLS playlist (index.m3u8)
    for a specific video resolution.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, resolution):
        """
        Return the HLS playlist file for a given video and resolution.

        :param movie_id: ID of the video
        :param resolution: Video resolution (e.g. 720p, 1080p)
        :return: M3U8 playlist file
        :raises Http404: If the playlist file does not exist
        """
        path = os.path.join(
            settings.MEDIA_ROOT,
            "hls",
            str(movie_id),
            resolution,
            "index.m3u8"
        )

        if not os.path.exists(path):
            raise Http404("Playlist not found")

        return FileResponse(
            open(path, "rb"),
            content_type="application/vnd.apple.mpegurl"
        )