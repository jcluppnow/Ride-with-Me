# pylint:disable=invalid-name, too-many-return-statements
"""
Contains the event participation view
"""
import asyncio

from django.http import Http404
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from channels.layers import get_channel_layer

from ..models import Event
from ..serializers import EventSerializer
from ..helpers import is_attending


@api_view(['POST', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.IsAuthenticated])
def participate(request, pk):
    """
    Add or remove current user as an event participant
    """
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist as error:
        raise Http404 from error

    attending = is_attending(request, event)

    if request.method == 'POST':
        # Make sure the user is not already participating in the event
        if attending:
            return Response(
                {'error': 'You are already participating in this event.'},
                status=HTTP_400_BAD_REQUEST
            )

        # Make sure the user is not organising this event
        if request.user == event.organiser:
            return Response(
                {'error': 'You are organising this event, and cannot be added as a participant.'},
                status=HTTP_400_BAD_REQUEST
            )

        # Make sure the event has not started
        if event.started:
            return Response(
                {'error': 'This event has started. No more participatants are permitted.'},
                status=HTTP_400_BAD_REQUEST
            )

        # Make sure the event is not at capacity
        if event.is_full:
            return Response(
                {'error': 'This event is full.'},
                status=HTTP_400_BAD_REQUEST
            )

        # Add this user as a participant
        event.participants.add(request.user)

        channel_layer = get_channel_layer()
        message = {
            'type': 'broadcast_attend_event',
            'data': {
                'event_id': str(event.event_id),
                'user_id': request.user.id
            }
        }

        asyncio.run(channel_layer.group_send(str(event.event_id), message))

        # Return updated event, with this user as a participant
        serializer = EventSerializer(event, context={'attending': True})
        return Response(serializer.data)

    if request.method == 'DELETE':
        # Make sure the user was participating in the event
        if not attending:
            return Response(
                {'error': 'You were not participating in this event.'},
                status=HTTP_400_BAD_REQUEST
            )

        # Remove this user as a participant
        event.participants.remove(request.user)

        channel_layer = get_channel_layer()
        message = {
            'type': 'broadcast_leave_event',
            'data': {
                'event_id': str(event.event_id),
                'user_id': request.user.id
            }
        }

        asyncio.run(channel_layer.group_send(str(event.event_id), message))

        # Return updated event, without this user as a participant
        serializer = EventSerializer(event, context={'attending': False})
        return Response(serializer.data)

    return None
