from django.apps import AppConfig


class PropertyConfig(AppConfig):
    name = 'afriproperty.property'

    def ready(self):
        try:
            import afriproperty.property.signals  # noqa F401
        except ImportError:
            pass
