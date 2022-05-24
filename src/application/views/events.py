"""
Contains the events view
"""

from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Event
from ..serializers import EventSerializer
from ..permissions import IsOwnerOrReadOnly


class Events(
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    """
    Create an event.
    """
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def post(self, request, *args, **kwargs):
        """
        Create a new event
        """
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Save the new event to the database.
        """
        serializer.save(organiser=self.request.user)
