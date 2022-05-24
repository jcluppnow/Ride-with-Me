"""
Contains the notification model class
"""

from django.contrib.gis.db import models

from .custom_user import CustomUser
from .event import Event

class Notification(models.Model):
    """
    Notification Model

    Attributes:
        notification_id     A unique identifier for the notification
        recipient           The user who receives the notification
        notifier            The user that initiated the notification
        content             The notification text
        event               The event the notification is related to
        read_at             When the notification was read
        type                The type of notification that this is
    """
    notification_id = models.AutoField(primary_key=True)
    recipient = models.ForeignKey(CustomUser, related_name='recipient', on_delete=models.CASCADE)
    notifier = models.ForeignKey(CustomUser, related_name='notifier', on_delete=models.CASCADE)
    content = models.TextField()
    event = models.ForeignKey(Event, related_name='event', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True)

    class NotificationType(models.TextChoices):
        """
        Types of possible notifications
        """
        # Standard notification that links to the event
        GENERAL = 'GEN'

        # Chat message
        MESSAGE = 'MSG'

        # Distance alert
        DISTANCE_ALERT = 'DST'

    type = models.CharField(
        max_length=3,
        choices=NotificationType.choices,
        default=NotificationType.GENERAL
    )
