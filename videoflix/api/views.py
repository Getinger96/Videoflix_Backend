from rest_framework.views import APIView
from .serializers import VideoSerializer
from videoflix.models import Video
from rest_framework.response import Response
from django.http import FileResponse, Http404
import os
from django.conf import settings
from rest_framework.permissions import IsAuthenticated




class VideoListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    



class VideoSegmentView(APIView):
     permission_classes = [IsAuthenticated]
     def get(self, request, movie_id, resolution, segment):
        # 1️⃣ Video prüfen
        try:
            video = Video.objects.get(pk=movie_id)
        except Video.DoesNotExist:
            raise Http404("Video not found")

        # 2️⃣ Pfad zum Segment bauen
        segment_path = os.path.join(
            settings.MEDIA_ROOT,
            "hls",
            str(movie_id),
            resolution,
            segment
        )

        # 3️⃣ Existenz prüfen
        if not os.path.exists(segment_path):
            raise Http404("Segment not found")

        # 4️⃣ TS-Datei streamen
        return FileResponse(
            open(segment_path, "rb"),
            content_type="video/MP2T"
        )
    

class VideoResolutionPlaylistView(APIView):
     permission_classes = [IsAuthenticated]
     def get(self, request, movie_id, resolution):
        path = os.path.join(
            settings.MEDIA_ROOT,
            "hls",
            str(movie_id),
            resolution,
            "index.m3u8"
        )

        if not os.path.exists(path):
            raise Http404()

        return FileResponse(
            open(path, "rb"),
            content_type="application/vnd.apple.mpegurl"
        )