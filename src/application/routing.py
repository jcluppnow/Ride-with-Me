"""
Define websocket url patterns
"""
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/ridewithme', consumers.EventConsumer.as_asgi()),
]
