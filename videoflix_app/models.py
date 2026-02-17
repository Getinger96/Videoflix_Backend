from django.db import models
from datetime import date


class Video(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title=models.CharField(max_length=80)
    descripition=models.CharField(max_length=250)
    thumbnail_url=models.FileField(upload_to='thumbnails/', null=True, blank=True)
    video_file=models.FileField(upload_to='videos/', null=True, blank=True)
    category=models.CharField(max_length=50, default='Uncategorized')