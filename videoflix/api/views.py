from rest_framework.views import APIView
from .serializers import VideoSerializer
from videoflix.models import Video
from rest_framework.response import Response



class VideoListView(APIView):
    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)