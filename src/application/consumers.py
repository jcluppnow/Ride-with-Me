"""
WebSocket consumer
"""
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework import serializers as rules
from webpush import send_user_notification
from .validator import Validator
from .models import Event, ChatMessage, CustomUser, Notification
from .serializers import EventSerializer, ChatMessageSerializer, NotificationSerializer
from .helpers import is_attending_user


def make_socket_error(message, request_id=""):
    """
    Generate a socket error response
    :param message: Error message
    :param request_id: Request ID
    """
    return json.dumps({
        'event': f'socketerror{request_id}',
        'data': {
            'error': message
        }
    })


def make_ack_response(request_id):
    """
    Generate a socket acknowledgement response
    :param request_id: Request ID to acknowledge
    """
    return json.dumps({
        'event': f'response{request_id}',
        'data': {
            'status': 'ok'
        }
    })


class EventConsumer(WebsocketConsumer):
    """
    Event WebSocket request consumer
    """

    def broadcast_start_event(self, broadcast_event):
        """
        On broadcast start event
        """
        user = self.scope["user"]

        try:
            event = Event.objects.get(pk=broadcast_event["data"]["event_id"])
            # For each user that isn't the organiser of the event, send a start_event event
            if user != event.organiser \
                    and is_attending_user(user, event):
                serializer = EventSerializer(
                    event,
                    context={'user': user}
                )

                self.send(text_data=json.dumps({
                    'event': 'eventstart',
                    'data': serializer.data
                }))
            return None
        except Event.DoesNotExist:
            # Silently ignore error
            return None

    def broadcast_finish_event(self, broadcast_event):
        """
        On broadcast finish event
        """
        user = self.scope["user"]

        try:
            event = Event.objects.get(pk=broadcast_event["data"]["event_id"])
            # For each user that isn't the organiser of the event, send a finish_event event
            if user != event.organiser and is_attending_user(user, event):
                serializer = EventSerializer(
                    event,
                    context={'user': user}
                )

                self.send(text_data=json.dumps({
                    'event': 'eventfinish',
                    'data': serializer.data
                }))
            return None
        except Event.DoesNotExist:
            # Silently ignore error
            return None

    def broadcast_attend_event(self, broadcast_event):
        """
        On broadcast start event
        """
        user = self.scope["user"]

        try:
            event = Event.objects.get(pk=broadcast_event["data"]["event_id"])

            if user.id != broadcast_event['data']['user_id'] and is_attending_user(user, event):
                serializer = EventSerializer(
                    event,
                    context={'user': user}
                )

                self.send(text_data=json.dumps({
                    'event': 'newparticipant',
                    'data': serializer.data
                }))
            return None
        except Event.DoesNotExist:
            # Silently ignore error
            return None

    def broadcast_leave_event(self, broadcast_event):
        """
        On broadcast start event
        """
        user = self.scope["user"]

        try:
            event = Event.objects.get(pk=broadcast_event["data"]["event_id"])

            if user.id != broadcast_event['data']['user_id'] and is_attending_user(user, event):
                self.send(text_data=json.dumps({
                    'event': 'participantleave',
                    'data': {
                         'user_id': broadcast_event['data']['user_id'],
                         'event_id': broadcast_event['data']['event_id'],
                    }
                }))
            return None
        except Event.DoesNotExist:
            # Silently ignore error
            return None

    def attend_event(self, request_id, data):
        """
        Add channel for newly attending event
        """

        user = self.scope["user"]

        # Get event object
        try:
            event = Event.objects.get(pk=data["event_id"])

            # Ensure user is attending the event
            if is_attending_user(user, event):
                async_to_sync(self.channel_layer.group_add)(
                    str(event.event_id),
                    self.channel_name
                )
                self.send(text_data=make_ack_response(request_id))
            else:
                self.send(text_data=make_socket_error(
                    "You are not attending this event.",
                    request_id=request_id
                ))

        except Event.DoesNotExist:
            # Send error
            self.send(text_data=make_socket_error(
                "Event does not exist.",
                request_id=request_id
            ))

    def leave_event(self, request_id, data):
        """
        Discard channel when leaving an event
        """

        # Get event object
        try:
            event = Event.objects.get(pk=data["event_id"])
            async_to_sync(self.channel_layer.group_discard)(
                str(event.event_id),
                self.channel_name
            )
            self.send(text_data=make_ack_response(request_id))
        except Event.DoesNotExist:
            # Send error
            self.send(text_data=make_socket_error(
                "Event does not exist.",
                request_id=request_id
            ))

    def broadcast_location(self, broadcast_event):
        """
        Broadcast the organiser's location to all connected participants
        """
        user = self.scope["user"]

        try:
            event = Event.objects.get(pk=broadcast_event["data"]["event_id"])
            if user != event.organiser:
                self.send(text_data=json.dumps({
                    'event': 'organiserlocation',
                    'data': broadcast_event["data"]
                }))
            return None
        except Event.DoesNotExist:
            # Silently ignore error
            return None

    def send_location(self, request_id, data):
        """
        Handler for the send location request. Receives and rebroadcasts the
        event organiser's location.
        """
        user = self.scope["user"]

        try:
            event = Event.objects.get(pk=data["event_id"])
            if user == event.organiser:
                # Send acknowledgement
                self.send(text_data=make_ack_response(request_id))

                # Broadcast the location
                async_to_sync(self.channel_layer.group_send)(
                    data["event_id"],
                    {
                        'type': 'broadcast_location',
                        'data': data
                    }
                )
            else:
                # Send error
                self.send(text_data=make_socket_error(
                    "You are not the organiser.",
                    request_id=request_id
                ))
        except Event.DoesNotExist:
            # Send error
            self.send(text_data=make_socket_error(
                "Event does not exist.",
                request_id=request_id
            ))

    def send_message(self, request_id, data):
        """
        Handler for the message send request.
        """

        user = self.scope["user"]

        try:
            event = Event.objects.get(pk=data["event_id"])

            if is_attending_user(user, event) and data["content"]:
                # Store the message
                message = ChatMessage(
                    content=data["content"],
                    sender=user,
                    event=event
                )

                message.save()

                # Broadcast the message
                async_to_sync(self.channel_layer.group_send)(
                    data["event_id"],
                    {
                        'type': 'broadcast_chat_message',
                        'data': {
                            'message_id': message.message_id
                        }
                    }
                )

                # Send acknowledgement
                serializer = ChatMessageSerializer(message)

                self.send(text_data=json.dumps({
                    'event': f'response{request_id}',
                    'data': serializer.data
                }))
            else:
                self.send(text_data=make_socket_error(
                    "Invalid request.",
                    request_id=request_id
                ))
        except Event.DoesNotExist:
            # Send error
            self.send(text_data=make_socket_error(
                "Event does not exist.",
                request_id=request_id
            ))

    def broadcast_chat_message(self, broadcast_event):
        """
        Broadcast a chat message to all connected participants
        """
        user = self.scope["user"]

        try:
            message = ChatMessage.objects.get(pk=broadcast_event["data"]["message_id"])

            if message.sender != user \
                    and is_attending_user(user, message.event):
                serializer = ChatMessageSerializer(message)

                self.send(text_data=json.dumps({
                    'event': 'chatmessage',
                    'data': serializer.data
                }))
            return None
        except ChatMessage.DoesNotExist:
            # Silently ignore error
            return None

    def send_alert(self, request_id, data):
        """
        Handler for a participant notifying that they are out of range
        """

        user = self.scope["user"]

        try:
            event = Event.objects.get(pk=data["event_id"])

            # Ensure the user is participating in this event
            if is_attending_user(user, event):
                # Forward notification to organiser
                async_to_sync(self.channel_layer.group_send)(
                    data["event_id"],
                    {
                        'type': 'broadcast_participant_alert',
                        'data': {
                            'event_id': data["event_id"],
                            'participant_id': user.id
                        }
                    }
                )

                notification = Notification(
                    event=event,
                    recipient=user,
                    notifier=event.organiser,
                    content="You are too far away from the organiser!")

                notification.save()

                self.send(text_data=json.dumps({
                    'event': f'response{request_id}',
                    'data': NotificationSerializer(notification).data
                }))

                payload = {
                    'head': 'Distance Alert',
                    'body': "You are too far away from the organiser!"
                }
                send_user_notification(user=user, payload=payload, ttl=1000)
            else:
                self.send(text_data=make_socket_error(
                    "You are not attending this event.",
                    request_id=request_id
                ))
        except Event.DoesNotExist:
            # Send error
            self.send(text_data=make_socket_error(
                "Event does not exist.",
                request_id=request_id
            ))

    def broadcast_participant_alert(self, broadcast_event):
        """
        Forward a participant distance alert to the organiser
        """
        user = self.scope["user"]

        try:
            event = Event.objects.get(pk=broadcast_event["data"]["event_id"])
            if user == event.organiser:
                participant_id = broadcast_event["data"]["participant_id"]
                participant = CustomUser.objects.get(pk=participant_id)

                notification = Notification(
                    event=event,
                    recipient=user,
                    notifier=participant,
                    content=f'{participant.full_name} is too far away!')

                notification.save()

                self.send(text_data=json.dumps({
                    'event': 'distancealert',
                    'data': {
                        'notification': NotificationSerializer(notification).data
                    }
                }))

                payload = {
                    'head': 'Distance Alert',
                    'body': f'{participant.full_name} is too far away!'
                }
                send_user_notification(user=user, payload=payload, ttl=1000)
            return None
        except Event.DoesNotExist:
            # Silently ignore error
            return None

    def connect(self):
        user = self.scope["user"]

        if user.is_authenticated is True:
            # connect to channel for each event
            # this should be filtered to stop connecting to channels for events that are no longer active
            self.accept()
            for event in user.participants.all() | user.organiser.all():
                async_to_sync(self.channel_layer.group_add)(
                    str(event.event_id),
                    self.channel_name
                )
            self.send(text_data=json.dumps({
                'event': 'connect',
                'data': 'connected'
            }))

    # Receive message from WebSocket
    def receive(self, text_data):  # pylint:disable=arguments-differ
        data = json.loads(text_data)

        validator = Validator({
            'request': rules.CharField(required=True),
            'request_id': rules.IntegerField(required=True)
        }, data).validate()

        user = self.scope["user"]
        if validator.passed and user.is_authenticated:
            if validator.validated_fields['request'] in self.request_types:
                self.request_types[validator.validated_fields['request']](self, data['request_id'], data['data'])
        elif user.is_authenticated is False:
            self.send(text_data=make_socket_error(
                "Unauthenticated",
            ))
            self.close()
        else:
            self.send(text_data=make_socket_error(
                "Invalid message received.",
            ))

    def disconnect(self, code):
        user = self.scope["user"]
        # For each event, leave the channel
        for event in user.participants.all() | user.organiser.all():
            async_to_sync(self.channel_layer.group_discard)(
                str(event.event_id),
                self.channel_name
            )

    request_types = {
        'attend_event': attend_event,
        'leave_event': leave_event,
        'send_location': send_location,
        'send_message': send_message,
        'send_participant_alert': send_alert
    }
