from django.db import models
from datetime import date


class Video(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title=models.CharField(max_length=80)
    descripition=models.CharField(max_length=250)
    video_file=models.FileField(upload_to='videos/', null=True, blank=True)