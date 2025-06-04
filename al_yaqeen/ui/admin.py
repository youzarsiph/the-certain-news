"""Admin site for Al Yaqeen"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from al_yaqeen.categories.models import Category
from al_yaqeen.users.models import User


# Create your model admins here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Extended UserAdmin"""


# Register your models here.
admin.site.register(Category)
