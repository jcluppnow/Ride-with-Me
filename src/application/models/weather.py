"""
Contains the weather model class.
"""
from django.contrib.gis.db import models
from .validators import validate_start_time

class Weather(models.Model):
    """
    Weather Model

    Attributes:
        weather_id          A universally-unique identifier for the event
        temperature         Temparature in celsius at a specific point
        humidity            Percentage humidity for this point
        precipitation       Chance of rain at this point
        wind_speed          The wind speed for this point
        wind_direction      The direction the wind is blowing at this point
        coordinates         The location for this weather
        weather_date        The date for when the weather is for
        created_at          When the object was first created
        updated_at          When the object was last updated
    """
    weather_id = models.BigAutoField(primary_key=True, editable=False)
    temperature = models.FloatField(null=True)
    humidity = models.FloatField(null=True)
    precipitation = models.FloatField(null=True)
    wind_speed = models.FloatField(null=True)
    wind_direction = models.IntegerField(null=True)
    coordinates = models.PointField()
    weather_date = models.DateTimeField(validators=[validate_start_time])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
