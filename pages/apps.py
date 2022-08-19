import atexit

from django.apps import AppConfig


class PagesConfig(AppConfig):
    name = 'pages'
    # verbose_name = 'Service'
    verbose_name = 'サービス'

    def ready(self):
        from . import signals
        from .extensions import schedule_processing
        signals.__name__
        schedule_processing.__name__
        atexit.register(lambda: schedule_processing.mmap_client.dispose(leave_file=True))
