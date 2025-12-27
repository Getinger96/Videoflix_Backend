from django.apps import AppConfig


class VideoflixConfig(AppConfig):
    name = 'videoflix'

    def ready(self):
        from . import signals
