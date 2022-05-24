"""
Custom forms for the Ride with Me application
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Creation form for the Ride with Me custom user model
    """

    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'profile')


class CustomUserChangeForm(UserChangeForm):
    """
    Change form for the Ride with Me custom user model
    """

    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'profile')


class RegisterForm(UserCreationForm):
    """
    Form for user registration
    """
    # Add full_name to form (default only includes user and pass)
    full_name = forms.CharField(max_length=255, required=True)

    class Meta:
        model = CustomUser
        fields = ("email", "full_name", "password1", "password2")
