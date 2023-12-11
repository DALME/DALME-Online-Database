"""Override the built-in auth.User model."""
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass
