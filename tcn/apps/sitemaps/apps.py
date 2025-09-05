"""AppConf for tcn.apps.sitemaps"""

from django.apps import AppConfig


# Create your AppConf here.
class SitemapsConfig(AppConfig):
    """App Configuration for tcn.apps.sitemaps"""

    label = "tcn_sitemaps"
    name = "tcn.apps.sitemaps"
    default_auto_field = "django.db.models.BigAutoField"
