"""
Contains the custom user model class
"""
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from ..managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model
    Adapted from https://testdriven.io/blog/django-custom-user-model/

    Attributes:
        email           The unique email address of the user
        full_name       The full name of the user
        is_staff        Whether this is a staff account
        is_active       Whether this account is active
        date_joined     The date this user joined
    """
    email = models.EmailField('Email address', unique=True)
    full_name = models.CharField(max_length=255)
    profile = models.ImageField(upload_to='uploads/profile_images', default='static/application/images/default-blue.png')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
