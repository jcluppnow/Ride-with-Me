# pylint:disable=invalid-name
"""
Contains the event chat view
"""
from datetime import timedelta
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from ..permissions import IsParticipating

from ..models import ChatMessage
from ..serializers import ChatMessageSerializer, EventMessageSerializer


class StandardResultsSetPagination(PageNumberPagination):
    """
    Pagination set with page size 15
    """
    page_size = 15
    max_page_size = 15

@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.IsAuthenticated, IsParticipating])
class EventChatView(ListAPIView): # pylint:disable=too-few-public-methods
    """
    Fetch historical chat messages for an event
    (New messages will be broadcast over socket connections as they arrive.)
    """
    pagination_class = StandardResultsSetPagination
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        """
        Return a list of all chat messages for an event to be paginated
        """
        event_id = self.kwargs['pk']
        return ChatMessage.objects.filter(event_id=event_id).order_by('-created_at')

@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.IsAuthenticated])
class ChatView(ListAPIView): # pylint:disable=too-few-public-methods
    """
    Fetch historical chat messages for all user events
    """

    def get(self, request, *args, **kwargs):
        """
        Get the messages for all user events
        """

        user = request.user
        cutoff_time = timezone.now() - timedelta(days=1)

        participating_events = user.participants.filter(finished=False, starting_time__gt=cutoff_time)

        organising_events = user.organiser.filter(finished=False, starting_time__gt=cutoff_time)

        user_events = participating_events.union(organising_events)

        serialized_events = []
        for event in user_events:
            serialized_events.append(EventMessageSerializer(event).data)

        return Response(serialized_events)
