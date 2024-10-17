from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # ได้รับแจ้งเตือนเกี่ยวกับการดำเนินการ
    def ready(self):
        import users.signals
    