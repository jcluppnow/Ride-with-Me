# pylint:disable=invalid-name
"""
Contains the start event view
"""
from datetime import timedelta
import asyncio

from django.http import Http404
from django.utils import timezone
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from channels.layers import get_channel_layer

from ..models import Event
from ..serializers import EventSerializer


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.IsAuthenticated])
def start_event(request, pk):
    """
    Mark an event as started
    """
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist as error:
        raise Http404 from error

    # Make sure the requesting user is the organiser
    if request.user != event.organiser:
        return Response(
            {'error': 'Only the organiser can start this event.'},
            status=HTTP_403_FORBIDDEN
        )

    # Make sure the event has not already been started
    if event.started:
        return Response(
            {'error': 'The event has already been started.'},
            status=HTTP_400_BAD_REQUEST
        )

    # Make sure it is not more than 0.5 hours before the designated event start time
    if not timezone.now() > (event.starting_time - timedelta(minutes=30)):
        return Response(
            {'error': 'You can not start this event yet.'},
            status=HTTP_400_BAD_REQUEST
        )

    # Start the event
    event.started = True
    event.save()

    channel_layer = get_channel_layer()
    message = {
        'type': 'broadcast_start_event',
        'data': {
            'event_id': str(event.event_id)
        }
    }

    asyncio.run(channel_layer.group_send(str(event.event_id), message))

    # Return updated event
    serializer = EventSerializer(
        event,
        context={'attending': True}
    )

    return Response(serializer.data)
