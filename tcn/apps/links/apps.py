"""AppConf for tcn.apps.links"""

from django.apps import AppConfig


# Create your config here.
class LinksConfig(AppConfig):
    """App configuration for tcn.apps.links"""

    name = "tcn.apps.links"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self) -> None:
        """Register signal receivers"""

        from tcn.apps.links.signals import register_link_signal_receivers

        register_link_signal_receivers()
