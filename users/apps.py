from django.apps import AppConfig                                                           # type:ignore


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # Переопределяем метод ready, который вызывается при готовности приложения
    def ready(self):
        import users.signals  # Импортируем модуль с сигналами для приложения 'users'
