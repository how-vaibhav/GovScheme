from django.apps import AppConfig


class SchemesappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'schemesapp'

    def ready(self):
        import schemesapp.signals
