from rest_framework import serializers
from videoflix.models import Video





class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Video
        fields=['id','created_at','title','descripition','thumbnail_url','category']