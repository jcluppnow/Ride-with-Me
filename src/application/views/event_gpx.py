# pylint:disable=invalid-name
"""
Contains the event GPX export view
"""

import gpxpy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from ..models import Event


def event_gpx(request, pk):
    """
    Export an event route to a GPX file
    """
    # Get event
    event = get_object_or_404(Event, pk=pk)
    route_coordinates = event.route_coordinates

    # Make GPX object
    gpx = gpxpy.gpx.GPX()

    # Set metadata
    gpx.name = event.name
    gpx.author_name = event.organiser.full_name

    # Create track
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    # Create segment
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    # Add points
    for coord in route_coordinates:
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(coord[1], coord[0]))

    # Add starting point as a waypoint
    start_waypoint = gpxpy.gpx.GPXWaypoint(
        event.starting_location[1],
        event.starting_location[0],
        time=event.starting_time,
        name="Starting Location"
    )

    gpx.waypoints.append(start_waypoint)

    response = HttpResponse(gpx.to_xml(), content_type='application/gpx+xml')
    return response
