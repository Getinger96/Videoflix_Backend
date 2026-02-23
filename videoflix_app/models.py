from django.db import models
from datetime import date


class Video(models.Model):
    CategoryChoices = [
        ('Action', 'Action'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'),
        ('Horror', 'Horror'),
        ('Sci-Fi', 'Sci-Fi'),
        ('Documentary', 'Documentary'),
        ('Animation', 'Animation'),
        ('Thriller', 'Thriller'),
        ('Romance', 'Romance'),
        ('Adventure', 'Adventure'),
        ('Fantasy', 'Fantasy'),
        ('Mystery', 'Mystery'),
        ('Crime', 'Crime'),
        ('Musical', 'Musical'),
        ('War', 'War'),
        ('Western', 'Western'),
        ('Other', 'Other'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    title=models.CharField(max_length=80)
    descripition=models.CharField(max_length=250)
    thumbnail_url=models.FileField(upload_to='thumbnails/', null=True, blank=True)
    video_file=models.FileField(upload_to='videos/', null=True, blank=True)
    category=models.CharField(max_length=50, choices=CategoryChoices, )