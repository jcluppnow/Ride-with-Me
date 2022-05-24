# pylint:disable=invalid-name
"""
Contains the event KML export view
"""

import simplekml
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from ..models import Event


def event_kml(request, pk):
    """
    Export an event route to a KML file
    """
    # Get event
    event = get_object_or_404(Event, pk=pk)
    route_coordinates = event.route_coordinates

    # Make KML object
    kml = simplekml.Kml()

    # Set metadata
    kml.document.name = event.name

    # Add LineString
    coords_list = []
    for coord in route_coordinates:
        coords_list.append((coord[0], coord[1]))

    line = kml.newlinestring(name="Event Route", coords=coords_list)

    # Style LineString
    line.style.linestyle.color = 'ff0000ff'
    line.style.linestyle.width = 10

    # Add starting point
    kml.newpoint(
        name="Starting Location",
        coords=[(event.starting_location[0], event.starting_location[1])]
    )

    response = HttpResponse(kml.kml(), content_type='application/vnd.google-earth.kml+xml')
    return response
