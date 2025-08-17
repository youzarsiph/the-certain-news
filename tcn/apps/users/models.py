"""Data Models for tcn.apps.users"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class User(AbstractUser):
    """Users"""

    country = CountryField(
        null=True,
        blank=True,
        help_text=_("User country"),
    )
    phone = PhoneNumberField(
        null=True,
        blank=True,
        help_text=_("User phone number"),
    )
    photo = models.ImageField(
        null=True,
        blank=True,
        help_text=_("Profile image"),
        upload_to="images/users/",
    )
    bio = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text=_("Tell us about yourself"),
    )
