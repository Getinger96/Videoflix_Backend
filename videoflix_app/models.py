from django.db import models
from datetime import date


CATEGORY_CHOICES = [
    ('Action', 'Action'),
    ('Comedy', 'Comedy'),
    ('Drama', 'Drama'),
    ('Horror', 'Horror'),
    ('Sci-Fi', 'Sci-Fi'),
    ('Documentary', 'Documentary'),
    ('Animation', 'Animation'),
    ('Thriller', 'Thriller'),
    ('Romance', 'Romance'),
    ('Fantasy', 'Fantasy'),
]

class Video(models.Model):
    """
    Represents an uploaded video with its associated metadata,
    thumbnail, video file and category.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=80)
    description = models.TextField(max_length=250)
    thumbnail_url = models.FileField(upload_to='thumbnails/', null=False, blank=False)
    video_file = models.FileField(upload_to='videos/', null=False, blank=False)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Action')
    

    def __str__(self):
        return self.title