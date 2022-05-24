"""
Integration tests for the event API
"""
import pytest

from django.utils import timezone
from django.core.management import call_command
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer
from rest_framework.test import APIClient
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
async def test_event_finish_receive_broadcast():
    """Test attendee will receive a broadcast_finish_event"""

    attendee = await sync_to_async(UserFactory.create)()
    event = await sync_to_async(EventFactory)(starting_time=timezone.now(), started=True, finished=True, participants=(attendee,))

    attendee_socket = AuthWebsocketCommunicator(EventConsumer.as_asgi(), '/ws/ridewithme', user=attendee)
    await attendee_socket.connect()

    await attendee_socket.receive_from(timeout=5) # clear socket

    message = {
        'type': 'broadcast_finish_event',
        'data': {
            'event_id': str(event.event_id)
        }
    }
    channel_layer = get_channel_layer()
    await channel_layer.group_send(str(event.event_id), message)

    response = await attendee_socket.receive_from(timeout=5)

    assert "eventfinish" in response

    await attendee_socket.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_non_existent_event_ignored():
    """Test attendee will not receive a broadcast_start_event for a non existent event"""

    attendee = await sync_to_async(UserFactory.create)()
    # Have user participate in an event to have a channel open
    await sync_to_async(EventFactory)(starting_time=timezone.now(), started=True, participants=(attendee,))

    attendee_socket = AuthWebsocketCommunicator(EventConsumer.as_asgi(), '/ws/ridewithme', user=attendee)
    await attendee_socket.connect()

    await attendee_socket.receive_from(timeout=5) # clear socket

    message = {
        'type': 'broadcast_finish_event',
        'data': {
            'event_id': "30e7764c-ceec-4192-9d65-299f82d33341"
        }
    }
    channel_layer = get_channel_layer()
    await channel_layer.group_send("30e7764c-ceec-4192-9d65-299f82d33341", message)

    await attendee_socket.receive_nothing()

    await attendee_socket.disconnect()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_event_finish_broadcast():
    """Test full finish event broadcast"""

    organiser = await sync_to_async(CustomUser.objects.first)()
    attendee = await sync_to_async(UserFactory.create)()
    fields={'organiser': organiser, 'starting_time': timezone.now(), 'started': True, 'finished': False, 'participants': (attendee,)}
    event = await sync_to_async(EventFactory)(**fields)

    api_client = APIClient()
    await sync_to_async(api_client.force_login)(organiser)

    attendee_socket = AuthWebsocketCommunicator(EventConsumer.as_asgi(), '/ws/ridewithme', user=attendee)
    await attendee_socket.connect()

    await attendee_socket.receive_from(timeout=5) # clear socket

    await sync_to_async(api_client.post)(f'/api/v1/events/{event.event_id}/finish')

    response = await attendee_socket.receive_from(timeout=5)
    assert "eventfinish" in response

    await attendee_socket.disconnect()
