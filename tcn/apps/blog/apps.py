"""AppConf for tcn.apps.blog"""

from django.apps import AppConfig


# Create your config here.
class BlogConfig(AppConfig):
    """App configuration for tcn.apps.blog"""

    name = "tcn.apps.blog"
    default_auto_field = "django.db.models.BigAutoField"
