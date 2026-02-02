from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import os
from .tasks import convert_all
import django_rq

from videoflix.models import Video
@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video wurde gespeichert')
    if created:
        print('New Video created')
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_all, instance.video_file.path, instance.id)    
    

    


@receiver(post_delete, sender = Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)