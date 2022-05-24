"""
Chat message WebSocket API integration tests
"""

import pytest
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer
from django.core.management import call_command
from django.utils import timezone

from .mock_socket_client import AuthWebsocketCommunicator
from ..consumers import EventConsumer
from ..factories import UserFactory, ChatMessageFactory, EventFactory
from ..models import ChatMessage

@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir, settings):  # pylint:disable=unused-argument
    """Fixture to execute asserts before and after a test is run"""
    call_command('seed', verbosity=0)

    yield


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chat_receive_broadcast():
    """
    Test that an attendee will receive a broadcasted chat messsage
    """

    attendee_1 = await sync_to_async(UserFactory)()
    attendee_2 = await sync_to_async(UserFactory)()
    event = await sync_to_async(EventFactory)(
        starting_time=timezone.now(),
        participants=(attendee_1, attendee_2)
    )

    chat_message = await sync_to_async(ChatMessageFactory)(
        content="ABCDEF",
        event=event,
        sender=attendee_2
    )

    attendee_socket = AuthWebsocketCommunicator(
        EventConsumer.as_asgi(),
        '/ws/ridewithme',
        user=attendee_1
    )

    await attendee_socket.connect()

    await attendee_socket.receive_from(timeout=5) # clear socket

    message = {
        'type': 'broadcast_chat_message',
        'data': {
            'message_id': chat_message.message_id
        }
    }

    channel_layer = get_channel_layer()
    print(channel_layer.groups)

    await channel_layer.group_send(
        str(event.event_id),
        message
    )

    response = await attendee_socket.receive_from(timeout=5)

    assert "chatmessage" in response
    assert chat_message.content in response

    await attendee_socket.disconnect()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chat_is_saved():
    """Test chat message is saved"""

    attendee = await sync_to_async(UserFactory.create)()
    event = await sync_to_async(EventFactory)(starting_time=timezone.now(), started=True, participants=(attendee,))

    attendee_socket = AuthWebsocketCommunicator(EventConsumer.as_asgi(), '/ws/ridewithme', user=attendee)
    await attendee_socket.connect()

    count = await sync_to_async(ChatMessage.objects.count)()

    assert count == 10

    request = f'{{"request":"send_message","data":{{"event_id": "{event.event_id}", "content": "Test message"}},"request_id":2485}}'
    await attendee_socket.send_to(text_data=request)

    await attendee_socket.receive_from(timeout=5) # clear socket

    response = await attendee_socket.receive_from(timeout=5)
    assert '"content": "Test message"' in response

    count = await sync_to_async(ChatMessage.objects.count)()

    assert count == 11

    await attendee_socket.disconnect()
