from django.apps import AppConfig

class BurgerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'burger'  # Должно совпадать с именем папки приложения

    def ready(self):
        # Импорт сигналов только после полной загрузки приложения
        from . import signals

