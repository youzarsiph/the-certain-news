"""AppConf for tcn.apps.categories"""

from django.apps import AppConfig


# Create your config here.
class CategoriesConfig(AppConfig):
    """App configuration for tcn.apps.categories"""

    name = "tcn.apps.categories"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self) -> None:
        """Register signal receivers"""

        from tcn.apps.signals import register_category_signal_receivers

        register_category_signal_receivers()
