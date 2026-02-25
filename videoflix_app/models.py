from django.db import models
from datetime import date


class Category(models.Model):
    """
    Represents a video category used to group and organize videos.
    """

    name = models.CharField(max_length=50, unique=True)
    """The unique name of the category (e.g. 'Sports', 'Music', 'Education')."""

    def __str__(self):
        """
        Return the string representation of the category.

        :return: The category name
        """
        return self.name


class Video(models.Model):
    """
    Represents an uploaded video with its associated metadata,
    thumbnail, video file and category.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    """Timestamp of when the video was uploaded. Set automatically on creation."""

    title = models.CharField(max_length=80)
    """The title of the video. Maximum 80 characters."""

    description = models.TextField(max_length=250)
    """A short description of the video. Maximum 250 characters."""

    thumbnail_url = models.FileField(upload_to='thumbnails/', null=False, blank=False)
    """The thumbnail image file for the video. Stored in the 'thumbnails/' directory."""

    video_file = models.FileField(upload_to='videos/', null=False, blank=False)
    """The actual video file. Stored in the 'videos/' directory."""

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='videos')
    """The category this video belongs to. Deletes video if the category is removed."""

    def __str__(self):
        """
        Return the string representation of the video.

        :return: The video title
        """
        return self.title