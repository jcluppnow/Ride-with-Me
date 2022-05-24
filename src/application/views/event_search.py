"""
Contains the event search view
"""
import json
from datetime import timedelta

from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from django.utils import timezone
from django.contrib.postgres.search import SearchVector

from ..models import Event
from ..serializers import SearchedEventSerializer


@api_view()
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def event_search(request):
    """
    Search for an event by title, description  and location contents.
    """

    search_text = request.query_params.get('search_text')

    if search_text is None:
        return Response(
            {'error': 'Parameter \'query\' is missing.'},
            status=HTTP_400_BAD_REQUEST
        )

    search_text = str(json.loads(search_text)["query"])

    cutoff_time = timezone.now() - timedelta(days=1)

    # Add location search & organiser name.
    queryset = Event.objects.annotate(search=SearchVector(
        'name',
        'description',
        '_location_string'
    )).filter(search=search_text, is_private=False, starting_time__gt=cutoff_time)

    # Convert results to required format.
    serializer = SearchedEventSerializer(
        queryset,
        context={'request': request},
        many=True
    )

    return Response(serializer.data)
