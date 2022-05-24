"""
Contains the view for requesting weather from cache or tomorrow.io.
"""
import os
import json
from datetime import timedelta
import requests
import pytz
from dateutil import parser

from django.utils import timezone
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND,  HTTP_500_INTERNAL_SERVER_ERROR

from ..models import Weather
from ..models import Event
from ..serializers import EventSerializer

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def weather(request):
    """
    Fetch the event and associated weather from database or tomorrow.io.
    """
    # Fetch fields from request.
    data = request.data
    event_id = data.get("eventId")
    centre_lat = data.get("lat")
    centre_long = data.get("long")
    weather_date = data.get("weatherDate")

    # Check if any of the fields are empty.
    if (not event_id or not centre_lat or not centre_long or not weather_date):
        return Response(
            {'error': 'Invalid query fields passed while fetching weather.'},
            status=HTTP_400_BAD_REQUEST
        )

    # Check if any of the fields are invalid.
    if None not in (centre_lat, centre_long, event_id, weather_date):
        # Convert weather location to a Point type.
        weather_location = Point(centre_long, centre_lat, srid=4326)

        # Filter for weather within the given bounding circle that has a matching date.
        queryset = Weather.objects.filter(
            coordinates__distance_lte=(weather_location, D(m=1)),
            weather_date=weather_date
        ) \
        .annotate(user_distance=Distance("coordinates", weather_location)) \
        .order_by('user_distance')

        # Check if the query set returns any elements.
        if queryset.exists():
            # Serialize the queryset.
            model = queryset[0]
            updated_event = update_event(event_id, model)

            serializer = EventSerializer(updated_event)

            # Return the Event containing the Weather.
            return Response(serializer.data)

        # Fetch the weather and store it in the database.
        # Convert the date to python formatting.
        converted_date = parser.parse(weather_date)

        # Check if the date is greater than the date 14 days from now.
        future_date = (timezone.now() + timedelta(days=14)).astimezone(pytz.utc)

        # Compare the two dates.
        if future_date > converted_date:
            # Construct the query.
            query = construct_query(centre_lat, centre_long, weather_date)

            # Execute the request using the query.
            response = execute_request(query)

            # Check if the request was succesful.
            if successful_request(response):
                # Convert from JSON to a python dictionary.
                data = parse_json(response)

                # Store the weather data in database.
                model = store_weather_data(data, centre_lat, centre_long, weather_date)
                model.save()

                # Update the related event with the weather data.
                updated_event = update_event(event_id, model)

                # Serialize the Event.
                serializer = EventSerializer(updated_event)

                return Response(serializer.data)

            # If the date is > 14 days in the future return the error response.
            return construct_error_response(response)
    return Response(
        {'error': 'Invalid query fields passed while fetching weather.'},
        status=HTTP_400_BAD_REQUEST
    )

def construct_query(latitude, longitude, starting_date):
    """
    Constructs the payload for the weather request.
    """
    location_string = str(longitude) + "," + str(latitude)

    # Fetch the API key.
    api_key = os.getenv('TOMORROWIO_API_KEY')

    # Build the query.
    query_string = { "location":location_string,"fields":["temperature","humidity","windSpeed","windDirection","precipitationProbability"],
    "units":"metric","timesteps":"1d", "startTime":str(starting_date), "apikey":api_key }

    return query_string

def execute_request(query_string):
    """
    Setup the request logistics and perform the request.
    """
    headers = {"Accept": "application/json"}
    url = "https://api.tomorrow.io/v4/timelines"

    # Execute the request.
    response = requests.request("GET", url, headers=headers, params=query_string)

    return response

def parse_json(response):
    """
    Extract response text and convert to JSON.
    """
    extracted = json.loads(response.text)

    # Parse the JSON.
    data = extracted["data"]["timelines"][0]["intervals"][0]["values"]

    return data

def successful_request(response):
    """
    Check for invalid status code.
    """
    if response.status_code >= 400:
        return False

    return True

def store_weather_data(data, lat, long, date):
    """
    Create the weather model.
    """
    location = Point(long, lat, srid=4326)
    model = Weather(temperature = float(data["temperature"]), humidity = float(data["humidity"]),
    precipitation = float(data["precipitationProbability"]), wind_speed = float(data["windSpeed"]), wind_direction = float(data["windDirection"]),
    coordinates = location, weather_date = date)

    return model

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
            {'error': 'Invalid tomorrow.io api key.'},
            status=HTTP_401_UNAUTHORIZED
        )

    if response.status_code == 403:
        return Response(
            {'error': 'Reached account limit - tomorrow.io.'},
            status=HTTP_403_FORBIDDEN
        )
    if response.status_code == 404:
        return Response(
            {'error': 'Endpoint not found - tomorrow.io.'},
            status=HTTP_404_NOT_FOUND
        )

    if response.status_code == 500:
        return Response(
            {'error': 'Unable to connect to tomorrow.io servers.'},
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response(
        {'error': 'Unknown problem with internal server.'},
        status=HTTP_500_INTERNAL_SERVER_ERROR
    )

def update_event(event_id, weather_model):
    """
    Fetch and update the event weather field.
    """
    # Fetch the Event from the database.
    event = Event.objects.get(event_id=event_id)

    # Update the weather field.
    event.weather = weather_model

    # Save the changes made to the event.
    event.save()

    return event
