from django.apps import AppConfig


class VideoflixConfig(AppConfig):
    name = 'videoflix_app'

    def ready(self):
        from . import signals
