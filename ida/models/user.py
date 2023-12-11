"""Override the built-in auth.User model."""
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'
