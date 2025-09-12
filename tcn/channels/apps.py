"""AppConf for tcn.channels"""

from django.apps import AppConfig


# Create your AppConf here.
class ChannelsConfig(AppConfig):
    """App Configuration for tcn.channels"""

    name = "tcn.channels"
    label = "tcn_channels"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self) -> None:
        """Register live feed signal"""

        from tcn.channels.signals import register_live_feed

        register_live_feed()
