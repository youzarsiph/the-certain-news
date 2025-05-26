"""Generic View Mixins for al_yaqeen.ui"""

from typing import Any
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse


# Create your mixins here.
class AdminUserMixin(UserPassesTestMixin):
    """Check if the user is an admin"""

    def test_func(self) -> bool | None:
        return self.request.user.is_staff


class AccountOwnerMixin(UserPassesTestMixin):
    """Check if the user is owner of the account"""

    def test_func(self) -> bool | None:
        return self.request.user == self.get_object()


class InstructorMixin(UserPassesTestMixin):
    """Check if the user is an instructor"""

    def test_func(self) -> bool | None:
        return self.request.user.is_instructor


class OwnerMixin:
    """Adds the owner automatically"""

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Add the owner of the object automatically"""

        object = form.save(commit=False)
        object.user = self.request.user

        return super().form_valid(form)


class UserFilterMixin:
    """Filters queryset by user"""

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(user_id=self.request.user.id)


class UserModulesMixin:
    """Filter modules by user"""

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(course__user_id=self.request.user.id)


class UserLessonsMixin:
    """Filter lessons by user"""

    def get_queryset(self) -> QuerySet[Any]:
        return (
            super().get_queryset().filter(module__course__user_id=self.request.user.id)
        )


class UserAIMixin:
    """Filter assignments and items by user"""

    def get_queryset(self) -> QuerySet[Any]:
        return (
            super()
            .get_queryset()
            .filter(lesson__module__course__user_id=self.request.user.id)
        )


class UserAssignmentsMixin:
    """Filter assignments by user"""

    def get_queryset(self) -> QuerySet[Any]:
        return (
            super()
            .get_queryset()
            .filter(lesson__module__course__user_id=self.request.user.id)
        )


class UserItemsMixin(UserAIMixin):
    """Filter items by user"""


class UserQuestionsMixin:
    """Filter questions by user"""

    def get_queryset(self) -> QuerySet[Any]:
        return (
            super()
            .get_queryset()
            .filter(assignment__lesson__module__course__user_id=self.request.user.id)
        )


class UserAnswersMixin:
    """Filter answers by user"""

    def get_queryset(self) -> QuerySet[Any]:
        return (
            super()
            .get_queryset()
            .filter(
                question__assignment__lesson__module__course__user_id=self.request.user.id
            )
        )
