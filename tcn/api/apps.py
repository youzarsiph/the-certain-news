"""AppConf for tcn.api"""

from django.apps import AppConfig


# Create your AppConf here.
class APIConfig(AppConfig):
    """App Configuration for tcn.api"""

    name = "tcn.api"
    default_auto_field = "django.db.models.BigAutoField"
