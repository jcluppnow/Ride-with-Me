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

from .mock_socket_client import AuthWebsocketCommunicator
from ..consumers import EventConsumer
# python3.8 -m pytest test_event_start_websocket.py -rP
# python3.8 -m pytest tests --cov=application -rP


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir, settings): # pylint:disable=unused-argument
    """Fixture to execute asserts before and after a test is run"""
    call_command('seed', verbosity=0)

    yield

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_attendee_connects_to_event_group():
    """Test attendee will receive a broadcast_start_event"""

    attendee = await sync_to_async(UserFactory.create)()

    attendee_socket = AuthWebsocketCommunicator(EventConsumer.as_asgi(), '/ws/ridewithme', user=attendee)
    await attendee_socket.connect()

    await attendee_socket.receive_from(timeout=5) # clear socket

    channel_layer = get_channel_layer()
    assert len(channel_layer.groups.keys()) == 0

    # Create an event that the user is participating in
    event = await sync_to_async(EventFactory)(starting_time=timezone.now(), started=True, participants=(attendee,))

    request = f'{{"request":"attend_event","data":{{"event_id": "{event.event_id}"}},"request_id":2485}}'
    await attendee_socket.send_to(text_data=request)

    response = await attendee_socket.receive_from(timeout=5)
    assert '"status": "ok"' in response

    channel_layer = get_channel_layer()
    assert len(channel_layer.groups.keys()) == 1

    await attendee_socket.disconnect()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_non_attendee_cannot_connect_to_event_group():
    """Test attendee will receive a broadcast_start_event"""

    attendee = await sync_to_async(UserFactory.create)()

    attendee_socket = AuthWebsocketCommunicator(EventConsumer.as_asgi(), '/ws/ridewithme', user=attendee)
    await attendee_socket.connect()

    await attendee_socket.receive_from(timeout=5) # clear socket

    channel_layer = get_channel_layer()

    assert len(channel_layer.groups.keys()) == 0

    # Create an event that the user is participating in
    event = await sync_to_async(EventFactory)(starting_time=timezone.now(), started=True)

    request = f'{{"request":"attend_event","data":{{"event_id": "{event.event_id}"}},"request_id":2485}}'
    await attendee_socket.send_to(text_data=request)

    response = await attendee_socket.receive_from(timeout=5)
    assert "You are not attending this event." in response

    channel_layer = get_channel_layer()

    assert len(channel_layer.groups.keys()) == 0

    await attendee_socket.disconnect()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_invalid_event_id_returns_error():
    """Test attendee will receive a broadcast_start_event"""

    attendee = await sync_to_async(UserFactory.create)()

    attendee_socket = AuthWebsocketCommunicator(EventConsumer.as_asgi(), '/ws/ridewithme', user=attendee)
    await attendee_socket.connect()

    await attendee_socket.receive_from(timeout=5) # clear socket

    channel_layer = get_channel_layer()

    assert len(channel_layer.groups.keys()) == 0

    # Create an event that the user is participating in
    await sync_to_async(EventFactory)(starting_time=timezone.now(), started=True, participants=(attendee,))

    request = {
        "request": "attend_event",
        "request_id": 2485,
        "data": {
            "event_id": "30e7764c-ceec-4192-9d65-299f82d33341"
        }
    }
    await attendee_socket.send_to(text_data=json.dumps(request))

    response = await attendee_socket.receive_from(timeout=5)
    assert "Event does not exist." in response

    channel_layer = get_channel_layer()

    assert len(channel_layer.groups.keys()) == 0

    await attendee_socket.disconnect()
