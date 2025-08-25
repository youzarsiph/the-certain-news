"""Data Models for tcn.apps.users"""

from secrets import token_urlsafe

from django.contrib.auth.models import AbstractUser
from django.db import IntegrityError, models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class User(AbstractUser):
    """Users"""

    slug = models.SlugField(
        unique=True,
        db_index=True,
        allow_unicode=True,
        verbose_name=_("slug"),
        help_text=_("Slug"),
    )
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

    def save(self, **kwargs) -> None:
        """Update slug value"""

        self.slug = slugify(self.username)

        if (
            update_fields := kwargs.get("update_fields")
        ) is not None and "username" in update_fields:
            kwargs["update_fields"] = {"slug"}.union(update_fields)

        try:
            super().save(**kwargs)

        except IntegrityError:
            self.slug = slugify(f"{self.username}-{token_urlsafe(4)}")
            super().save(**kwargs)
