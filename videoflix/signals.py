from django.db.models.signals import post_save
from django.dispatch import receiver
@receiver(post_save, sender=Video)

def video_post_save(sender, instance, created, **kwargs):
    print('Video wurde gespeichert')
    if created:
        print('New Video created')