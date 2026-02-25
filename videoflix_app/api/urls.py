from django.urls import path, include
from .views import VideoListView, VideoSegmentView, VideoResolutionPlaylistView



urlpatterns = [
    path('video/', VideoListView.as_view(), name='video_list'),
    path('video/<int:movie_id>/<str:resolution>/<str:segment>/', VideoSegmentView.as_view(), name='video_segment'),
    path(
        "api/video/<int:movie_id>/<str:resolution>/index.m3u8",
        VideoResolutionPlaylistView.as_view(),
        name="video-playlist"
    ),
    ]

