from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # load signals เมื่อแอปเริ่มต้น
    def ready(self):
        import users.signals

    