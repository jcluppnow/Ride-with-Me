# pylint:disable=unused-import
# This warning is not applicable to our application
"""
Configures what models are accessible from the Django administration interface.
"""
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis import admin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Event, CustomUser, ChatMessage, Weather

admin.site.register(Event)
admin.site.register(ChatMessage)
admin.site.register(Weather)


class CustomUserAdmin(UserAdmin):
    """
    Admin form for the Ride with Me custom user model
    Adapted from https://testdriven.io/blog/django-custom-user-model/
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = (
        'email',
        'full_name',
        'profile',
        'is_staff',
        'is_active'
    )

    list_filter = (
        'email',
        'full_name',
        'is_staff',
        'is_active'
    )

    fieldsets = (
        (None,{'fields': ('email', 'password', 'full_name', 'profile')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'full_name',
                'profile',
                'password1',
                'password2',
                'is_staff',
                'is_active'
            )}
         ),
    )
    search_fields = ('email', 'full_name')
    ordering = ('email', 'full_name')


admin.site.register(CustomUser, CustomUserAdmin)
