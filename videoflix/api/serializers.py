from rest_framework import serializers
from videoflix.models import Video





class VideoSerializer(serializers.ModelSerializer):
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
            'descripition',
            'thumbnail_url',
            'category',
        ]

