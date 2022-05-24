"""
Integration tests for the event API
"""
import json
import pytest
from django.utils import timezone
from django.core.management import call_command
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer
from application.factories import EventFactory, UserFactory
from application.models import CustomUser

from .mock_socket_client import AuthWebsocketCommunicator
from ..consumers import EventConsumer
from ..models import CustomUser
# python3.8 -m pytest test_event_start_websocket.py -rP
# python3.8 -m pytest tests --cov=application -rP


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir, settings): # pylint:disable=unused-argument
    """Fixture to execute asserts before and after a test is run"""
    call_command('seed', verbosity=0)

    yield


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_location_receive_broadcast():
    """Test attendee will receive a broadcast_start_event"""

    attendee = await sync_to_async(UserFactory.create)()
    event = await sync_to_async(EventFactory)(starting_time=timezone.now(), started=True, finished=True, participants=(attendee,))

    attendee_socket = AuthWebsocketCommunicator(EventConsumer.as_asgi(), '/ws/ridewithme', user=attendee)
    await attendee_socket.connect()

    await attendee_socket.receive_from(timeout=5) # clear socket

    message = {
        'type': 'broadcast_location',
        'data': {
            'event_id': str(event.event_id),
            "latitude": 115,
            "longitude": -31
        }
    }
    channel_layer = get_channel_layer()
    await channel_layer.group_send(str(event.event_id), message)

    response = await attendee_socket.receive_from(timeout=5)

    assert "organiserlocation" in response
    assert '"latitude": 115, "longitude": -31' in response

    await attendee_socket.disconnect()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_location_broadcast():
    """Test attendee will receive a broadcast_start_event"""

    organiser = await sync_to_async(CustomUser.objects.first)()
    attendee = await sync_to_async(UserFactory.create)()

    fields = { 'organiser': organiser, 'starting_time': timezone.now(), 'started': True, 'finished': False, 'participants': (attendee,) }
    event = await sync_to_async(EventFactory)(**fields)

    organiser_socket = AuthWebsocketCommunicator(EventConsumer.as_asgi(), '/ws/ridewithme', user=organiser)
    await organiser_socket.connect()

    attendee_socket = AuthWebsocketCommunicator(EventConsumer.as_asgi(), '/ws/ridewithme', user=attendee)
    await attendee_socket.connect()

    await attendee_socket.receive_from(timeout=5) # clear socket

    request = {
        "request": "send_location",
        "request_id":2485,
        "data": {
            "event_id": str(event.event_id),
            "latitude": 115,
            "longitude": -31
        }
    }

    await organiser_socket.send_to(text_data=json.dumps(request))

    response = await attendee_socket.receive_from(timeout=5)

    assert "organiserlocation" in response

    assert '"latitude": 115, "longitude": -31' in response

    await attendee_socket.disconnect()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_invalid_event_id_returns_error():
    """Test attendee will receive a broadcast_start_event"""

    organiser = await sync_to_async(CustomUser.objects.first)()
    attendee = await sync_to_async(UserFactory.create)()
    fields={'organiser': organiser, 'starting_time': timezone.now(), 'started': True, 'finished': False, 'participants': (attendee,)}
    await sync_to_async(EventFactory)(**fields)

    organiser_socket = AuthWebsocketCommunicator(EventConsumer.as_asgi(), '/ws/ridewithme', user=organiser)
    await organiser_socket.connect()

    attendee_socket = AuthWebsocketCommunicator(EventConsumer.as_asgi(), '/ws/ridewithme', user=attendee)
    await attendee_socket.connect()

    await attendee_socket.receive_from(timeout=5) # clear socket
    await organiser_socket.receive_from(timeout=5) # clear socket

    request = {
        "request":"send_location",
        "request_id":2485,
        "data": {
            "event_id": "30e7764c-ceec-4192-9d65-299f82d33341",
            "latitude": 115,
            "longitude": -31
        }
    }
    await organiser_socket.send_to(text_data=json.dumps(request))

    response = await organiser_socket.receive_from(timeout=5)
    assert "socketerror" in response

    response = await attendee_socket.receive_nothing()

    await attendee_socket.disconnect()
