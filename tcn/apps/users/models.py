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
        verbose_name=_("country"),
        help_text=_("User country"),
    )
    phone = PhoneNumberField(
        null=True,
        blank=True,
        verbose_name=_("phone number"),
        help_text=_("User phone number"),
    )
    photo = models.ImageField(
        null=True,
        blank=True,
        verbose_name=_("image"),
        upload_to="images/users/",
        help_text=_("Profile image"),
    )
    bio = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name=_("bio"),
        help_text=_("Tell us about yourself"),
    )
