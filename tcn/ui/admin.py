"""Admin site for TCN"""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from tcn.apps.links.models import Link

User = get_user_model()


# Create your model admins here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Extended UserAdmin"""


admin.site.register(Link)
