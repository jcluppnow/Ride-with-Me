# pylint:disable=invalid-name
"""
Contains the finish event view
"""
from django.http import Http404
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from ..models import Event
from ..serializers import EventSerializer


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.IsAuthenticated])
def finish_event(request, pk):
    """
    Mark an event as finished
    """
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist as error:
        raise Http404 from error

    # Make sure the requesting user is the organiser
    if request.user != event.organiser:
        return Response(
            {'error': 'Only the organiser can finish this event.'},
            status=HTTP_403_FORBIDDEN
        )

    # Make sure the event has been started
    if not event.started:
        return Response(
            {'error': 'The event has not been started.'},
            status=HTTP_400_BAD_REQUEST
        )

    # Make sure the event has not already been finished
    if event.finished:
        return Response(
            {'error': 'The event has already been finished.'},
            status=HTTP_400_BAD_REQUEST
        )

    # Start the event
    event.finished = True
    event.save()

    channel_layer = get_channel_layer()
    message = {
        'type': 'broadcast_finish_event',
        'data': {
            'event_id': str(event.event_id)
        }
    }
    async_to_sync(channel_layer.group_send)(str(event.event_id), message)

    # Return updated event
    serializer = EventSerializer(
        event,
        context={'attending': True}
    )

    return Response(serializer.data)
