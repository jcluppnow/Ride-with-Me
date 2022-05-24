# pylint:disable=invalid-name, unused-argument
"""
Contains miscellaneous, non-API views
"""
import json
from json import JSONDecodeError
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from application.factories import EventFactory, ChatMessageFactory
from ..helpers import testing_only
from ..serializers import EventSerializer, ChatMessageSerializer


@require_http_methods(["GET"])
def spa(request, url):
    """
    Returns the single-page application static page.
    """
    return render(request, 'application/spa.html')


@require_http_methods(["GET"])
def get_csrf(request):
    """
    Returns a CSRF token
    """
    return JsonResponse({'token': get_token(request)})


@login_required
def index(request):
    """
    Check if user is authenticated, if not redirects to accounts/login
    """
    return render(request, "/accounts/login")


@testing_only
def cypress_seed(request):
    """
    Seed database for testing
    """
    return JsonResponse({'seeded': call_command('cypress_seed')})


@testing_only
def create_event(request):
    """
    Seed database for testing
    """
    data = {}
    try:
        data = json.loads(request.body.decode('UTF-8'))
    except JSONDecodeError:
        # If the body is empty, then return an empty dict
        data = {}
    event = EventFactory(**data)
    serializer = EventSerializer(
        event
    )
    return JsonResponse({'create_event': serializer.data})


@testing_only
def create_message(request):
    """
    Seed database for testing
    """
    data = {}
    try:
        data = json.loads(request.body.decode('UTF-8'))
    except JSONDecodeError:
        # If the body is empty, then return an empty dict
        data = {}
    chat_message = ChatMessageFactory(**data)
    serializer = ChatMessageSerializer(
        chat_message
    )
    return JsonResponse({'create_chat_message': serializer.data})


@testing_only
def create_message_batch(request):
    """
    Seed database for testing
    """
    data = {}
    try:
        data = json.loads(request.body.decode('UTF-8'))
    except JSONDecodeError:
        # If the body is empty, then return an empty dict
        data = {}
    batch_size = data.pop('batch_size')
    chat_message = ChatMessageFactory.create_batch(batch_size, **data)
    serializer = ChatMessageSerializer(
        chat_message, many=True
    )
    return JsonResponse({'create_chat_message': serializer.data})
