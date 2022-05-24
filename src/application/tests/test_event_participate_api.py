"""
Integration tests for the event API
"""
from django.test import TestCase
from django.utils import timezone
from django.core.management import call_command

from rest_framework.test import APIClient

from application.models import CustomUser
from application.factories import EventFactory


class EventParticipateIntegrationTestCases(TestCase):
    """
    Participate API test cases
    """

    def setUp(self):
        call_command('seed', verbosity=0)
        self.api_client = APIClient()
        self.api_client.force_login(CustomUser.objects.first())

    def test_can_participate(self):
        """Test user can participate in an event"""

        event = EventFactory()

        response = self.api_client.post(f'/api/v1/events/{event.event_id}/participate')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'"event_id":"{event.event_id}"'.encode())
        self.assertContains(response, '"attending":true')

    def test_can_leave(self):
        """Test user can leave an event"""

        event = EventFactory(participants=(CustomUser.objects.first(),))

        response = self.api_client.delete(f'/api/v1/events/{event.event_id}/participate')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'"event_id":"{event.event_id}"'.encode())
        self.assertContains(response, '"attending":false')

    def test_cannot_attend_while_attending(self):
        """Test user cannot attend while attending an event"""

        event = EventFactory(participants=(CustomUser.objects.first(),))

        response = self.api_client.post(f'/api/v1/events/{event.event_id}/participate')

        self.assertEqual(response.status_code, 400)

    def test_cannot_attend_after_event_started(self):
        """Test user cannot attend after event started"""

        event = EventFactory(starting_time=timezone.now(), started=True)

        response = self.api_client.post(f'/api/v1/events/{event.event_id}/participate')

        self.assertEqual(response.status_code, 400)

    def test_can_leave_after_event_started(self):
        """Test user can leave after event started"""

        event = EventFactory(
            starting_time=timezone.now(),
            started=True,
            participants=(CustomUser.objects.first(),)
        )

        response = self.api_client.delete(f'/api/v1/events/{event.event_id}/participate')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'"event_id":"{event.event_id}"'.encode())
        self.assertContains(response, '"attending":false')
