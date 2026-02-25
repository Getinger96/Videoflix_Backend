from rest_framework.views import APIView
from .serializers import VideoSerializer
from videoflix_app.models import Video
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
        serializer = VideoSerializer(videos, many=True,context={'request': request})
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
        # Falls URL index.m3u8/000.ts oder index.m3u8/003.ts
        if segment.startswith("index.m3u8/"):
            segment_file = segment.split("/", 1)[1]  # nur 000.ts, 001.ts etc.
        else:
            segment_file = segment

        file_path = os.path.join(settings.MEDIA_ROOT, 'hls', str(movie_id), resolution, segment_file)

        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), content_type='video/MP2T')
        raise Http404("Segment not found")

    
    
class VideoResolutionPlaylistView(APIView):
    """
    API view for serving the HLS playlist (index.m3u8)
    for a specific video resolution.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, resolution):
        path = os.path.join(settings.MEDIA_ROOT, 'hls', str(movie_id), resolution, 'index.m3u8')
        if not os.path.exists(path):
            raise Http404("Playlist not found")
        return FileResponse(open(path, 'rb'), content_type='application/vnd.apple.mpegurl')