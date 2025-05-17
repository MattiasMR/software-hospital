from django.apps import AppConfig


class BoxesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'boxes'

    def ready(self):
        # Importa esto para registrar los signals
        import boxes.signals  # noqa