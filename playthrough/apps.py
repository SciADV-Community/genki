from django.apps import AppConfig


class PlaythroughConfig(AppConfig):
    name = 'playthrough'

    def ready(self):
        import playthrough.signals  # noqa: F401
