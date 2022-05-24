# pylint:disable=invalid-name, unused-argument
"""
Contains the event detail view
"""

from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from ..models import Event
from ..serializers import EventSerializer
from ..permissions import IsOwnerOrReadOnly


class EventDetail(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView):
    """
    Get, update, or delete an event.
    """

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, pk):
        """
        Get the details of an event
        """
        event = self.get_object()

        serializer = EventSerializer(event, context={'request': request})
        serialized_data = serializer.data
        return Response(serialized_data)

    def put(self, request, *args, **kwargs):
        """
        Alter the details of an event
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Delete an event
        """
        return self.destroy(request, *args, **kwargs)
