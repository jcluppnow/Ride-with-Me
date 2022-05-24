"""
Contains the traffic model class
"""
from django.contrib.gis.db import models

class Traffic(models.Model):
    """
    Traffic Model

    Attributes:
        traffic_id          A universally-unique identifier for the traffic
        description         A overall description of the traffic
        start_date          The date the traffic started
        end_date            The projected end date of the traffic
        last_updated        The last time traffic was updated
        road_closed         Whether the traffic has caused a road closure
        severity            The recorded severity of the traffic
        traffic_type        A identifier for the type of traffic event e.g., traffic or congestion
        verified            Whether the event has been visually verified by local police
        coordinates         The coordinates for a traffic event
        created_at          When the object was first created
        updated_at          When the object was last updated
    """
    traffic_id = models.BigAutoField(primary_key=True, editable=False)
    description = models.TextField(null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    last_updated = models.DateTimeField()
    road_closed = models.BooleanField(default=False)
    severity = models.IntegerField()
    traffic_type = models.IntegerField()
    verified = models.BooleanField(default=False)
    coordinates = models.PointField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
