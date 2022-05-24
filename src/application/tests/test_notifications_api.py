"""
Integration tests for the notifications API
"""
from django.core.management import call_command
from django.test import TestCase

from rest_framework.test import APIClient

from application.models import Notification, CustomUser
from application.factories import NotificationFactory


class TestNotificationIntegrationTestCases(TestCase):
    """
    Notifications API test cases
    """

    def setUp(self):
        call_command('seed', verbosity=0)
        self.api_client = APIClient()
        self.api_client.force_login(CustomUser.objects.first())

    def test_notification_returned(self):
        """
        Test that an unread notification is returned
        """
        response = self.api_client.get('/api/v1/notifications')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

        notification = NotificationFactory(
            recipient=CustomUser.objects.first(),
            type=Notification.NotificationType.GENERAL
        )

        response = self.api_client.get('/api/v1/notifications')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'"notification_id":{notification.notification_id}'.encode())

    def test_notification_cleared(self):
        """
        Test that a cleared notification is not returned
        """
        _ = NotificationFactory(
            recipient=CustomUser.objects.first(),
            type=Notification.NotificationType.GENERAL
        )

        response = self.api_client.delete('/api/v1/notifications')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, None)

    def test_event_link_general(self):
        """
        Test that a notification of type general returns a link to the event
        """
        notification = NotificationFactory(
            recipient=CustomUser.objects.first(),
            type=Notification.NotificationType.GENERAL
        )

        response = self.api_client.get('/api/v1/notifications')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'"link":"/events#{notification.event.event_id}"'.encode())

    def test_event_link_chat(self):
        """
        Test that a notification of type chat message returns a link to the event chat page
        """
        notification = NotificationFactory(
            recipient=CustomUser.objects.first(),
            type=Notification.NotificationType.MESSAGE
        )

        response = self.api_client.get('/api/v1/notifications')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'"link":"/chat#{notification.event.event_id}"'.encode())
