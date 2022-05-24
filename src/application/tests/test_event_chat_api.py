"""
Integration tests for the event chat API
"""
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.core.management import call_command

from rest_framework.test import APIClient

from application.models import CustomUser
from application.factories import EventFactory, UserFactory, ChatMessageFactory


class EventChatAPITestCases(TestCase):
    """
    Chat API test cases
    """

    def setUp(self):
        call_command('seed', verbosity=0)
        self.api_client = APIClient()
        self.api_client.force_login(CustomUser.objects.first())

    def test_organiser_can_get_messages(self):
        """
        Test that an event organiser can fetch messages for that event
        """
        event = EventFactory(
            starting_time=(timezone.now() - timedelta(minutes=1)),
            participants=(CustomUser.objects.first(),)
        )

        self.api_client.force_login(event.organiser)

        response = self.api_client.get(f"/api/v1/events/{event.event_id}/chat")
        self.assertEqual(response.status_code, 200)


    def test_participant_can_get_messages(self):
        """
        Test that an event participant can fetch messages for that event
        """
        event = EventFactory(
            starting_time=(timezone.now()),
            participants=(CustomUser.objects.first(),)
        )

        response = self.api_client.get(f"/api/v1/events/{event.event_id}/chat")
        self.assertEqual(response.status_code, 200)


    def test_non_participant_cannot_get_messages(self):
        """
        Test that a user that is not organising or participating in an event
        cannot fetch messages for that event
        """
        event = EventFactory(
            starting_time=(timezone.now()),
            participants=(CustomUser.objects.first(),)
        )

        user = UserFactory()

        self.api_client.force_login(user)

        response = self.api_client.get(f"/api/v1/events/{event.event_id}/chat")
        self.assertEqual(response.status_code, 403)


    def test_response_does_not_contain_other_messages(self):
        """
        Test that a response containing chat messages for an event does not
        contain the messages for other events
        """
        event_1 = EventFactory(
            starting_time=(timezone.now()),
            participants=(CustomUser.objects.first(),)
        )

        chat_message_1 = ChatMessageFactory(event=event_1)

        event_2 = EventFactory(
            starting_time=(timezone.now()),
            participants=(CustomUser.objects.first(),)
        )

        chat_message_2 = ChatMessageFactory(event=event_2)

        response = self.api_client.get(f"/api/v1/events/{event_1.event_id}/chat")

        self.assertContains(response, f'"message_id":{chat_message_1.message_id}')
        self.assertNotContains(response, f'"message_id":{chat_message_2.message_id}')
