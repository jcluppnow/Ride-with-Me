"""
Contains the nearby events view
"""

from datetime import timedelta

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point, Polygon
from django.contrib.gis.measure import D
from django.utils import timezone
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from ..models import Event
from ..serializers import EventSerializer


@api_view()
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def nearby_events(request):
    """
    Get nearby events
    """
    # Filter to only show events happening today or in the future
    cutoff_time = timezone.now() - timedelta(days=1)

    # Query type 1 -- get events from a bounding box formed of a NE/SW
    # coordinate pair
    ne_lat = request.query_params.get('ne_lat')
    ne_long = request.query_params.get('ne_long')
    sw_lat = request.query_params.get('sw_lat')
    sw_long = request.query_params.get('sw_long')

    if None not in (ne_lat, ne_long, sw_lat, sw_long):
        # Make bounding box
        bounding_box = (sw_long, sw_lat, ne_long, ne_lat)
        bounding_polygon = Polygon.from_bbox(bounding_box)

        # Query for events with a starting location within the box
        queryset = Event.objects.filter(
            starting_location__coveredby=bounding_polygon,
            starting_time__gt=cutoff_time,
            is_private=False,
        )

        serializer = EventSerializer(
            queryset,
            context={'request': request},
            many=True
        )

        return Response(serializer.data)

    # Query type 2 -- get events based on a centre lat/long and a distance limit
    lat = request.query_params.get('lat')
    long = request.query_params.get('long')
    distance = request.query_params.get('distance')

    if None not in (lat, long, distance):
        # Filter for events within the given bounding circle
        user_location = Point(float(long), float(lat), srid=4326)
        queryset = Event.objects.filter(
            starting_location__distance_lte=(user_location, D(m=distance)),
            starting_time__gt=cutoff_time,
            is_private=False) \
            .annotate(user_distance=Distance("starting_location", user_location)) \
            .order_by('user_distance')

        serializer = EventSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    # If the required query params are not present, error
    return Response(
        {'error': 'Request is missing required query parameters.'},
        status=HTTP_400_BAD_REQUEST
    )
