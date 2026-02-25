from django.db import models
from datetime import date


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Video(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True)
    title=models.CharField(max_length=80)
    description=models.TextField(max_length=250)
    thumbnail_url=models.FileField(upload_to='thumbnails/', null=False, blank=False)
    video_file=models.FileField(upload_to='videos/', null=False, blank=False)
    category=models.ForeignKey(Category, on_delete=models.CASCADE,related_name='videos')
     
    def __str__(self):
        return self.title