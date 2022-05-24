"""
Integration tests for the event API
"""
from datetime import timedelta

from django.utils import timezone
from django.test import TestCase
from django.core.management import call_command

from rest_framework.test import APIClient

from application.factories import EventFactory
from application.models import CustomUser


class EventStartIntegrationTestCases(TestCase):
    """
    Event start API test cases
    """

    def setUp(self):
        call_command('seed', verbosity=0)
        self.api_client = APIClient()

    def test_can_start_after_start_time(self):
        """Test organiser can start an event"""

        event = EventFactory(starting_time=(timezone.now() - timedelta(minutes=15)))
        organiser = event.organiser
        self.api_client.force_login(organiser)

        response = self.api_client.post(f'/api/v1/events/{event.event_id}/start')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'"event_id":"{event.event_id}"'.encode())
        self.assertContains(response, '"attending":true')

    def test_cannot_start_one_hour_before_start_time(self):
        """Test organiser cannot start before start time"""

        event = EventFactory(starting_time=(timezone.now() + timedelta(minutes=59)))
        organiser = event.organiser
        self.api_client.force_login(organiser)

        response = self.api_client.post(f'/api/v1/events/{event.event_id}/start')

        self.assertEqual(response.status_code, 400)

    def test_only_organiser_can_start_event(self):
        """Test only organiser can start an event"""

        event = EventFactory()

        self.api_client.force_login(CustomUser.objects.first())

        response = self.api_client.post(f'/api/v1/events/{event.event_id}/start')

        self.assertEqual(response.status_code, 403)

    def test_can_start_half_hour_before_start_time(self):
        """Test can start half an hour before start time"""

        event = EventFactory(starting_time=(timezone.now() + timedelta(minutes=15)))

        self.api_client.force_login(event.organiser)

        response = self.api_client.post(f'/api/v1/events/{event.event_id}/start')

        self.assertEqual(response.status_code, 200)
