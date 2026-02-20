from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class CaseInsensitiveAuth:
    """
    Authenticate using username OR email (case-insensitive)
    """

    def authenticate(self, request, username_or_email=None, password=None):
        if username_or_email is None or password is None:
            return None

        try:
            user = User.objects.get(
                Q(username__iexact=username_or_email) |
                Q(email__iexact=username_or_email)
            )
        except User.DoesNotExist:
            return None

        if user.check_password(password) and user.is_active:
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
