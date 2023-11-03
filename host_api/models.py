from typing import Optional, Any

from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from django.db import models
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.
            extra_fields (dict): Additional fields for the user.

        Returns:
            User: The created user.

        Raises:
            ValueError: If the email is not provided.
        """
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(
        self, email: str, password: Optional[str] = None, **extra_fields: Any
    ):
        """
        Create and save a regular User with the given email and password.

        Args:
            email (str): The email of the user.
            password (str, optional): The password of the user. Defaults to None.
            **extra_fields: Additional fields to be passed to the _create_user method.

        Returns:
            User: The created user object.
        """
        # Set default values for additional fields
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        # Call the _create_user method with the provided arguments and additional fields
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.

        Args:
            email (str): The email of the superuser.
            password (str): The password of the superuser.
            **extra_fields: Additional fields to set for the superuser.

        Raises:
            ValueError: If the 'is_staff' field is not set to True or if the 'is_superuser' field is not set to True.

        Returns:
            User: The created superuser instance.
        """
        # Set default values for 'is_staff' and 'is_superuser' fields
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Check if 'is_staff' field is set to True
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        # Check if 'is_superuser' field is set to True
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        # Create the superuser using the _create_user method
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    subscribe = models.ManyToManyField(
        to="self", blank=True, related_name="followers", symmetrical=False
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
