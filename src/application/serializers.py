"""
Model object serializers for use with Django REST Framework
"""

from rest_framework import serializers
from .models import Event, CustomUser, Weather, ChatMessage, Traffic, Notification
from .helpers import is_attending, is_attending_user


class FullUserSerializer(serializers.ModelSerializer):
    """
    User details serializer that adds all fields, including private information
    """

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'full_name',
            'profile'
        ]


class BasicUserSerializer(serializers.ModelSerializer):
    """
    User details serializer that excludes private fields
    """

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'full_name',
            'profile'
        ]


class ChatMessageSerializer(serializers.ModelSerializer):
    """
    Chat message serializer
    """

    class Meta:
        model = ChatMessage
        fields = [
            'message_id',
            'sender_id',
            'created_at',
            'content',
            'sender',
            'event_id'
        ]

    sender = BasicUserSerializer(read_only=True)
    event_id = serializers.UUIDField()


class EventMessageSerializer(serializers.ModelSerializer):
    """
    Serialize messages by event
    """

    class Meta:
        model = Event
        fields = [
            'event_id',
            'messages'
        ]

    messages = ChatMessageSerializer(many=True, source='latest_messages')


class WeatherResponseSerializer(serializers.ModelSerializer):
    """
    Weather data serializer that returns a weather object excluding
    creational timestamps
    """

    class Meta:
        model = Weather
        fields = [
            'weather_id',
            'temperature',
            'humidity',
            'precipitation',
            'wind_speed',
            'wind_direction',
            'weather_date'
        ]


class TrafficSerializer(serializers.ModelSerializer):
    """
    Traffic data serializer that returns a traffic object excluding
    creational timestamps
    """

    class Meta:
        model = Traffic
        fields = [
            'traffic_id',
            'description',
            'start_date',
            'end_date',
            'last_updated',
            'road_closed',
            'severity',
            'traffic_type',
            'verified',
            'coordinates'
        ]

class SearchedEventSerializer(serializers.ModelSerializer):
    """
    Event data serializer
    """

    class Meta:
        model = Event
        fields = [
            'event_id',
            'name',
            'organiser',
            'hero_image',
        ]

        read_only_fields = [
            'organiser',
        ]

    organiser = BasicUserSerializer(read_only=True)


class EventSerializer(serializers.ModelSerializer):
    """
    Event data serializer
    """

    class Meta:
        model = Event
        fields = [
            'event_id',
            'name',
            'is_private',
            'description',
            'attending',
            'checked_in',
            'organiser',
            'weather',
            'max_participants',
            'is_full',
            'hero_image',
            'average_speed',
            'starting_time',
            'started',
            'finished',
            'distance',
            'duration',
            'participants',
            'check_ins',
            'starting_location',
            'route_coordinates',
            'created_at',
            'updated_at',
            'location_string'
        ]

        read_only_fields = [
            'organiser',
            'participants',
            'check_ins',
            'started',
            'location_string'
        ]

    attending = serializers.SerializerMethodField()
    checked_in = serializers.SerializerMethodField()
    organiser = BasicUserSerializer(read_only=True)
    participants = BasicUserSerializer(many=True, read_only=True)
    weather = WeatherResponseSerializer(read_only=True)

    def get_attending(self, obj):
        """
        Determine whether the requesting user is attending this event
        """
        if self.context.get('attending') is not None:
            # If the attendance status has been manually set, use that
            return self.context.get('attending')

        if self.context.get('request'):
            # Otherwise, get the user from the request, and determine whether
            # they are attending this event
            request = self.context.get('request')
            return is_attending(request, obj)

        if self.context.get('user'):
            # Check if a user was passed in, and determine whether
            # they are checked in to this event
            user = self.context.get('user')
            return is_attending_user(user, obj)

        return None

    def get_checked_in(self, obj):
        """
        Determine whether the requesting user is checked in to this event
        """
        if self.context.get('checked_in') is not None:
            # If the check-in status has been manually set, use that
            return self.context.get('checked_in')

        if self.context.get('request'):
            # Otherwise, get the user from the request, and determine whether
            # they are checked in to this event
            user = self.context.get('request').user
            return obj.check_ins.filter(id=user.id).exists()

        if self.context.get('user'):
            # Check if a user was passed in, and determine whether
            # they are checked in to this event
            user = self.context.get('user')
            return obj.check_ins.filter(id=user.id).exists()

        return None


class NotificationSerializer(serializers.ModelSerializer):
    """
    Notification serializer
    """

    class Meta:
        model = Notification
        fields = [
            'notification_id',
            'notifier_id',
            'notifier',
            'link',
            'content',
            'event_id',
            'event',
            'read_at',
            'created_at'
        ]

    event = EventSerializer(read_only=True)
    event_id = serializers.UUIDField()
    link = serializers.SerializerMethodField()
    notifier = BasicUserSerializer(read_only=True)

    def get_link(self, obj):  # pylint:disable=no-self-use
        """
        Generate the link
        """
        if obj.type == Notification.NotificationType.MESSAGE:
            return f"/chat#{obj.event.event_id}"

        return f"/events#{obj.event.event_id}"
