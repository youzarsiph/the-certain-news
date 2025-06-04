"""Chooser ViewSets"""

from django.utils.translation import gettext_lazy as _
from wagtail.admin.viewsets.chooser import ChooserViewSet


# Create your chooser viewsets here.
class CategoryChooserViewSet(ChooserViewSet):
    """Category chooser view set"""

    icon = "folder"
    model = "categories.Category"
    choose_one_text = _("Choose a Category")
    edit_item_text = _("Edit this Category")
    choose_another_text = _("Choose another Category")
    form_fields = ["name", "description"]


viewsets = {"categories": CategoryChooserViewSet("category_chooser")}
