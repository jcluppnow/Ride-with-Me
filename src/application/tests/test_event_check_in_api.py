"""
Integration tests for the event API
"""
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.core.management import call_command

from rest_framework.test import APIClient

from application.models import CustomUser
from application.factories import EventFactory


class EventCheckInIntegrationTestCases(TestCase):
    """
    Check-in API test cases
    """

    def setUp(self):
        call_command('seed', verbosity=0)
        self.api_client = APIClient()
        self.api_client.force_login(CustomUser.objects.first())

    def test_can_check_in_after_start_59(self):
        """Test user can check in to an event"""

        event = EventFactory(starting_time=(timezone.now() + timedelta(minutes=59)),
                             participants=(CustomUser.objects.first(),))

        response = self.api_client.post(f'/api/v1/events/{event.event_id}/check_in')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'"event_id":"{event.event_id}"'.encode())
        self.assertContains(response, '"checked_in":true')

    def test_can_check_in_after_start_1(self):
        """Test user can check in to an event"""

        event = EventFactory(starting_time=(timezone.now() - timedelta(minutes=1)),
                             participants=(CustomUser.objects.first(),))

        response = self.api_client.post(f'/api/v1/events/{event.event_id}/check_in')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'"event_id":"{event.event_id}"'.encode())
        self.assertContains(response, '"checked_in":true')

    def test_cannot_check_in_longer_than_one_hour_before_start(self):
        """Test user cannot check in when longer than one hour before start"""

        event = EventFactory(starting_time=(timezone.now() + timedelta(hours=2)),
                             participants=(CustomUser.objects.first(),))

        response = self.api_client.post(f'/api/v1/events/{event.event_id}/check_in')

        self.assertEqual(response.status_code, 400)

    def test_organiser_cannot_check_in(self):
        """Test organiser cannot check in to an event"""

        event = EventFactory(starting_time=(timezone.now() + timedelta(hours=2)),
                             participants=(CustomUser.objects.first(),))

        self.api_client.force_login(event.organiser)

        response = self.api_client.post(f'/api/v1/events/{event.event_id}/check_in')

        self.assertEqual(response.status_code, 400)
