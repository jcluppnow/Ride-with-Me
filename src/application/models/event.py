# pylint:disable=no-member
"""
Contains the event model class
"""
import uuid
from copy import copy

from django.contrib.gis.db import models
from django.core.validators import MinValueValidator

from .custom_user import CustomUser
from .validators import validate_start_time
from .weather import Weather
from ..services import ReverseGeocoder

class Event(models.Model):
    """
    Event Model

    Attributes:
        event_id            A universally-unique identifier for the event
        average_speed       An organiser-defined average speed for the event
        route_coordinates   The coordinates of all points in the event route
        name                The event name
        max_participants    An organiser-defined maximum number of allowed event participants
        participants        Users participating in the event
        description         The event description
        starting_time       The event start time
        started             Whether the organiser has started the event
        is_private          Whether the event is hidden from the public directory
        organiser           The user organising the event
        starting_location   The point where the event will start
        hero_image          The event hero image
        created_at          When the object was first created
        updated_at          When the object was last updated
        _location_string    Private backing storage for the location_string property
    """
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    average_speed = models.IntegerField(null=True, validators=[MinValueValidator(1)])
    route_coordinates = models.LineStringField()
    name = models.TextField()
    max_participants = models.IntegerField(null=True, validators=[MinValueValidator(1)])
    participants = models.ManyToManyField(CustomUser, related_name="participants")
    check_ins = models.ManyToManyField(CustomUser, related_name="check_ins")
    description = models.TextField(null=True)
    starting_time = models.DateTimeField(validators=[validate_start_time])
    started = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    is_private = models.BooleanField()
    organiser = models.ForeignKey(CustomUser, related_name="organiser", on_delete=models.CASCADE)
    weather = models.ForeignKey(Weather, related_name="weather", on_delete=models.CASCADE, null=True)
    starting_location = models.PointField()
    hero_image = models.ImageField(upload_to='uploads/hero_images', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    _location_string = models.TextField(null=True)

    @property
    def distance(self):
        """
        :return: The calculated distance of the event route in metres
        """
        line = copy(self.route_coordinates)
        line.srid = 4326

        # Transform to the line to a projected coordinate system, so the length can be measured
        line.transform(3857)

        return line.length

    @property
    def duration(self):
        """
        :return: The calculated duration of the event in seconds
        """
        # Convert speed to metres/second
        speed_ms = float(self.average_speed) / 3.6

        return self.distance / speed_ms

    @property
    def is_full(self):
        """
        :return: Whether the event is at capacity.
        """

        return self.participants.count() >= self.max_participants

    @property
    def owner(self):
        """
        :return: The owner of this object. (Used for generic API permissions.)
        """
        return self.organiser


    def latest_messages(self):
        """
        Get the latest 15 messages for the event
        """
        return self.messages.all().order_by('-message_id')[:15]

    @property
    def location_string(self):
        """
        :return: The reverse-geocoded human description of the event location
        """

        rg_service = ReverseGeocoder()

        # Lazily evaluate the location string
        if self._location_string is None:
            result = rg_service.search((self.starting_location.y, self.starting_location.x))[0]
            self._location_string = f"{result['name']}, {result['admin1']}"
            self.save()

        return self._location_string

    def __str__(self):
        return self.name
