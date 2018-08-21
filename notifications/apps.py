from django.apps import AppConfig
import atexit

class NotificationsConfig(AppConfig):
    name = 'notifications'
    slack_thread = None

    def ready(self):
        pass
