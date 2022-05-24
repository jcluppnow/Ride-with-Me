"""
Contains the attending events view
"""
from datetime import timedelta

from django.utils import timezone
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from ..models import Event
from ..serializers import EventSerializer


@api_view()
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.IsAuthenticated])
def attending_events(request):
    """
    Get the events the current user is attending
    """
    # Filter to only show events happening today or in the future
    cutoff_time = timezone.now() - timedelta(days=1)

    queryset = Event.objects.filter(starting_time__gt=cutoff_time) \
               & (Event.objects.filter(participants=request.user)
                  | Event.objects.filter(organiser=request.user))

    serializer = EventSerializer(
        queryset,
        context={
            'attending': True,
            'request': request
        },
        many=True
    )

    return Response(serializer.data)
