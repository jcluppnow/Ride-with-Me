"""
Contains the chat message model class
"""
from django.contrib.gis.db import models

from .custom_user import CustomUser
from .event import Event


class ChatMessage(models.Model):
    """
    Chat Message Model

    Attributes:
        message_id          A universally-unique identifier for the message
        content             The content of the chat message
        sender           The unique ID of the sender of the chat message
        event             The unique event ID of the event the chat message is associated with
        created_at          The date the chat message was created
        updated_at          The date the chat message was updated
    """
    message_id = models.AutoField(primary_key=True)
    content = models.TextField()
    sender = models.ForeignKey(CustomUser, related_name="messages", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name="messages", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
