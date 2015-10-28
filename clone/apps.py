from django.apps import AppConfig

class HandlerConfig(AppConfig):
    name = 'clone'
    verbose_name = "Clone"

    def ready(self):
        import clone.signals.handlers