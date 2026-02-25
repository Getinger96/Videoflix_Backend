from rest_framework import serializers
from videoflix_app.models import Video





class VideoSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()
    """
    Serializer for the Video model.

    Converts Video model instances into JSON representations
    and validates incoming data for video-related API requests.
    """

    class Meta:
        
        """
        Meta configuration for VideoSerializer.
        """
        model = Video
        fields = [
            'id',
            'created_at',
            'title',
            'description',
            'thumbnail_url',
            'category',
        ]

    def get_thumbnail_url(self, obj):
         request = self.context.get('request')
         if request is not None:
            return request.build_absolute_uri(obj.thumbnail_url.url)
         return obj.thumbnail_url.url


    
