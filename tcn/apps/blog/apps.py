"""AppConf for tcn.apps.blog"""

from django.apps import AppConfig


# Create your config here.
class BlogConfig(AppConfig):
    """App configuration for tcn.apps.blog"""

    name = "tcn.apps.blog"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self) -> None:
        """Register signal receivers"""

        from tcn.apps.signals import register_post_signal_receivers

        register_post_signal_receivers()
