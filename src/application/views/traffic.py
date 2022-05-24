"""
Contains the view for requesting traffic from cache or Bing.
"""
import os
import json
from datetime import datetime, timedelta
import requests


from django.contrib.gis.geos import Polygon
from django.utils import timezone
from django.contrib.gis.geos import Point

from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_503_SERVICE_UNAVAILABLE

from ..models import Traffic
from ..serializers import TrafficSerializer

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def traffic(request):
    """
    Fetch the traffic data from a specific bounding box.
    """
    # Filter to only show events happening today or in the future
    cutoff_time = timezone.now() - timedelta(days=1)

    ne_lat = request.query_params.get('ne_lat')
    ne_long = request.query_params.get('ne_long')
    sw_lat = request.query_params.get('sw_lat')
    sw_long = request.query_params.get('sw_long')

    # Check if the fields are valid.
    if None not in (ne_lat, ne_long, sw_lat, sw_long):
        # Make a bounding box using fields.
        bounding_box = (sw_long, sw_lat, ne_long, ne_lat)
        bounding_polygon = Polygon.from_bbox(bounding_box)

        # Return traffic objects within the bounding box and after or on the start date.
        queryset = Traffic.objects.filter(
            coordinates__coveredby=bounding_polygon,
            start_date__gt=cutoff_time
        )

        # Check if there are any results from the database.
        if queryset.exists():

            # Serialize the results.
            serializer = TrafficSerializer(
                queryset,
                context={'request', request},
                many=True
            )

            # Return the serialized data.
            return Response(serializer.data)

        # If there are no serialized events, fetch from Bing API.
        query_string = construct_query(ne_lat, ne_long, sw_lat, sw_long)

        # Execute the request using the query string.
        response = execute_request(query_string)

        if successful_request(response):
            # Convert from JSON to a python dictionary.
            data = parse_json(response)

            # Create an store traffic data. Then return an array of all models.
            traffic_data = store_traffic_data(data)

            # Serialize traffic data to be returned.
            serializer = TrafficSerializer(
                traffic_data,
                context={'request': request},
                many=True
            )

            return Response(serializer.data)

        # If the request was unsuccesful, return the relevant error code.
        return construct_error_response(response)

    # If the fields are not valid, return an invalid response
    return Response(
        {'error': 'Invalid query fields.'},
        status=HTTP_400_BAD_REQUEST
    )

def construct_query(ne_lat, ne_long, sw_lat, sw_long):
    """
    Constructs the payload for the traffic request.
    """
    # Fetch the API key.
    api_key = os.getenv('BING_TRAFFIC_API_KEY')

    # Append key to required format.
    key_string = "?key=" + str(api_key)

    # Append coords to required format.
    location_string = str(sw_lat) + "," + str(sw_long) + "," + str(ne_lat) + "," + str(ne_long)

    # Build query string.
    query_string = "http://dev.virtualearth.net/REST/v1/Traffic/Incidents/" + location_string + key_string

    return query_string

def execute_request(query_string):
    """
    Execute the request using the query string.
    """
    headers = {"Accept": "application/json"}

    # Execute the request and store the response.
    response = requests.request("GET", query_string, headers=headers)

    return response

def successful_request(response):
    """
    Check for invalid status code.
    """
    if response.status_code >= 400:
        return False

    return True

def construct_error_response(response):
    """
    Handle all possible status codes from tomorrow.io.
    """
    if response.status_code == 400:
        return Response(
            {'error': 'Invalid query fields.'},
            status=HTTP_400_BAD_REQUEST
        )

    if response.status_code == 401:
        return Response(
            {'error': 'Invalid Bing api key.'},
            status=HTTP_401_UNAUTHORIZED
        )

    if response.status_code == 404:
        return Response(
            {'error': 'Endpoint not found - Bing.'},
            status=HTTP_404_NOT_FOUND
        )

    if response.status_code == 500:
        return Response(
            {'error': 'Unable to connect to Bing servers.'},
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )

    if response.status_code == 503:
        return Response(
            {'error': 'Unable to connect to Bing, service unavailable.'},
            status=HTTP_503_SERVICE_UNAVAILABLE
        )

    return Response(
        {'error': 'Unknown problem with internal server.'},
        status=HTTP_500_INTERNAL_SERVER_ERROR
    )

def parse_json(response):
    """
    Extract response text and convert to JSON.
    """
    extracted = json.loads(response.text)

    # Parse the JSON.
    data_array = extracted["resourceSets"][0]["resources"]

    return data_array

def store_traffic_data(data):
    """
    Create and store the traffic model.
    """
    traffic_data = []

    # Iterate over traffic events.
    for current_traffic_event in data:
        # Extract fields from traffic event.
        # Extract location data and convert to point.
        point = current_traffic_event["point"]["coordinates"]
        location = Point(point[0], point[1], srid=4326)
        description = current_traffic_event["description"]
        start_date = convert_date(current_traffic_event["start"])
        end_date = convert_date(current_traffic_event["end"])
        last_updated = convert_date(current_traffic_event["lastModified"])
        road_closed = current_traffic_event["roadClosed"] == "true"
        severity = int(current_traffic_event["severity"])
        traffic_type = int(current_traffic_event["type"])
        verified = current_traffic_event["verified"] == "true"

        # Create traffic model using the fields.
        model = Traffic(description=description, start_date=start_date, end_date=end_date,
        last_updated=last_updated, road_closed=road_closed, severity=severity, traffic_type=traffic_type,
        verified=verified, coordinates=location)

        traffic_data.append(model)

        # Save the new Traffic model.
        model.save()

    return traffic_data

def convert_date(date_string):
    """
    Convert string from seconds from 1970 to a datetime object.
    """
    # Tokenize and extract as an integer.
    date = int(date_string.split("(")[1].split(")")[0])
    date = date/1000
    converted_date = datetime.fromtimestamp(date)

    return converted_date
