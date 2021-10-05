from django.apps import AppConfig


class TipsConfig(AppConfig):
    name = 'afriproperty.tips'

    def ready(self):
        try:
            import afriproperty.tips.signals  # noqa F401
        except ImportError:
            pass
