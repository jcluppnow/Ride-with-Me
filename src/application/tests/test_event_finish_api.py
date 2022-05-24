"""
Integration tests for the event API
"""
from django.utils import timezone
from django.test import TestCase
from django.core.management import call_command

from rest_framework.test import APIClient

from application.factories import EventFactory
from application.models import CustomUser


class EventFinishIntegrationTestCases(TestCase):
    """
    Event finish API test cases
    """

    def setUp(self):
        call_command('seed', verbosity=0)
        self.api_client = APIClient()

    def test_can_finish_after_start(self):
        """Test organiser can finish an event"""

        event = EventFactory(starting_time=timezone.now(), started=True)
        organiser = event.organiser
        self.api_client.force_login(organiser)

        response = self.api_client.post(f'/api/v1/events/{event.event_id}/finish')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'"event_id":"{event.event_id}"'.encode())

    def test_cannot_finish_a_finished_event(self):
        """Test organiser cannot finish an event that is already finished"""

        event = EventFactory(started=True, finished=True)
        organiser = event.organiser
        self.api_client.force_login(organiser)

        response = self.api_client.post(f'/api/v1/events/{event.event_id}/finish')

        self.assertEqual(response.status_code, 400)

    def test_cannot_finish_an_event_without_start(self):
        """Test organiser cannot finish before start"""

        event = EventFactory()
        organiser = event.organiser
        self.api_client.force_login(organiser)

        response = self.api_client.post(f'/api/v1/events/{event.event_id}/finish')

        self.assertEqual(response.status_code, 400)

    def test_only_organiser_can_finish_event(self):
        """Test only organiser can finish an event"""

        event = EventFactory()

        self.api_client.force_login(CustomUser.objects.first())

        response = self.api_client.post(f'/api/v1/events/{event.event_id}/finish')

        self.assertEqual(response.status_code, 403)
