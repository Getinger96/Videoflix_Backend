from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import os
from .tasks import convert_all
import django_rq

from videoflix.models import Video
@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    Signal handler triggered after a Video instance is saved.

    If a new Video is created:
    - Enqueue a background task to convert the uploaded video
      into all required formats (e.g. HLS resolutions).
    """

    print('Video was saved')

    if created:
        print('New Video created')

        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(
            convert_all,
            instance.video_file.path,
            instance.id
        )


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Signal handler triggered after a Video instance is deleted.

    Automatically removes the associated video file from
    the file system to prevent orphaned files.
    """

    if instance.video_file and os.path.isfile(instance.video_file.path):
        os.remove(instance.video_file.path)