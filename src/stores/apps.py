from django.apps import AppConfig


class StoresConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stores'

    def ready(self) -> None:
        import stores.signals 
