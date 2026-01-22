from django.urls import path, include
from .views import VideoListView



urlpatterns = [
    path('videos/', VideoListView.as_view(), name='video_list'),
    
]

