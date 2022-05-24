# pylint:disable=invalid-name
"""
Contains the event check in view
"""
from datetime import timedelta

from django.http import Http404
from django.utils import timezone
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from ..models import Event
from ..serializers import EventSerializer
from ..helpers import is_attending


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.IsAuthenticated])
def check_in(request, pk):
    """
    Check in the current user to an event
    """
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist as error:
        raise Http404 from error

    checked_in = event.check_ins.filter(id=request.user.id).exists()
    attending = is_attending(request, event)

    # Make sure the user has not already checked in to the event
    if checked_in:
        return Response(
            {'error': 'You have already checked in to this event.'},
            status=HTTP_400_BAD_REQUEST
        )

    # Make sure the user is participating in this event
    if not attending:
        return Response(
            {'error': 'You are not participating in this event.'},
            status=HTTP_400_BAD_REQUEST
        )

    # Make sure the check-in attempt is not made more than 1 hour before start
    if (event.starting_time - timezone.now()) > timedelta(hours=1):
        return Response(
            {'error': 'You can only check in to an event within an hour of the starting time.'},
            status=HTTP_400_BAD_REQUEST
        )

    # Make sure the event has not been started
    if event.started:
        return Response(
            {'error': 'You can not check in to an event that has started.'},
            status=HTTP_400_BAD_REQUEST
        )

    # Check in this user
    event.check_ins.add(request.user)

    # Return updated event, with this user checked in
    serializer = EventSerializer(
        event,
        context={'attending': True, 'checked_in': True}
    )
    return Response(serializer.data)
