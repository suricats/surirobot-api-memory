from django.apps import AppConfig
import atexit

class NotificationsConfig(AppConfig):
    name = 'notifications'
    slack_thread = None

    def ready(self):
        from .realtime import SlackNotificationsThread
        self.slack_thread = SlackNotificationsThread(interval=10)
        # stop the thread at exit
        atexit.register(self.slack_thread.stop)
        # self.slack_thread.start()
