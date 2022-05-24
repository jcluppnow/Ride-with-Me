"""
Custom model validators
"""
from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_start_time(value):
    """
    Validates that an event start time value is in the past
    """
    if value < timezone.now():
        raise ValidationError("An event can not be created in the past")

    return value
