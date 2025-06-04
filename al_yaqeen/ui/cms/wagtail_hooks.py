"""Wagtail Hooks used to customize the view-level behavior of the Wagtail admin and front-end"""

from wagtail import hooks

from al_yaqeen.ui.cms.views.choosers import viewsets


# Create your hooks here.
@hooks.register("register_admin_viewset")
def register_views():
    return [*viewsets.values()]


@hooks.register("construct_explorer_page_queryset")
def show_my_pages_only(parent_page, pages, request):
    """Filter pages by user"""

    return pages.filter(owner=request.user)


@hooks.register("construct_document_chooser_queryset")
def show_my_uploaded_documents_only(documents, request):
    """Filter docs by user"""

    return documents.filter(uploaded_by_user_id=request.user.id)


@hooks.register("construct_image_chooser_queryset")
def show_my_uploaded_images_only(images, request):
    """Filter images by user"""

    return images.filter(uploaded_by_user_id=request.user.id)
