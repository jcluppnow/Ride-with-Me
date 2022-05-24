"""
Utility helper functions
"""
from functools import wraps
from django.conf import settings
from django.http import JsonResponse


def is_attending(request, event) -> bool:
    """
    Determine whether the requesting user is attending an event
    """
    # Organisers are counted as attendees
    if request.user == event.organiser:
        return True

    # If the user is not the organiser, check whether they are participating
    if event.participants.filter(id=request.user.id).exists():
        return True

    return False


def is_attending_user(user, event) -> bool:
    """
    Determine whether the given user is attending an event
    """
    # Organisers are counted as attendees
    if user == event.organiser:
        return True

    # If the user is not the organiser, check whether they are participating
    if event.participants.filter(id=user.id).exists():
        return True

    return False

def testing_only(func):
    """
    Enables route only in testing environment
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if settings.ENV == 'testing' and settings.DEBUG is True:
            return func(request, *args, **kwargs)
        return JsonResponse({'failed': 'not available'})
    return wrapper
