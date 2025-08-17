"""Forms for tcn.ui"""

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# User model
User = get_user_model()


# Create your forms here.
class UserCreateForm(UserCreationForm):
    """Custom form for creating users"""

    class Meta(UserCreationForm.Meta):
        """Meta data"""

        model = User
