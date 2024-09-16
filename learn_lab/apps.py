from django.apps import AppConfig


class LearnLabConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'learn_lab'

    def ready(self, *args, **kwargs):
        import learn_lab.signals  # noqa
        super_ready = super().ready(*args, **kwargs)
        return super_ready
