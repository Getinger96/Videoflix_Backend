from rest_framework.views import APIView
from .serializers import VideoSerializer
from videoflix.models import Video
from rest_framework.response import Response



class VideoListView(APIView):
    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    



class VideoSegmentView(APIView):
    def get(self, request, movie_id,resolution, segment):
        try:
            video = Video.objects.get(pk=movie_id)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=404)

        serializer = VideoSerializer(video)
        return Response(serializer.data)