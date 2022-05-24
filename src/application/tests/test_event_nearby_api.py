"""
Integration tests for the event api.
"""
from django.test import TestCase
from django.core.management import call_command
from django.contrib.gis.geos import LineString, Point

from rest_framework.test import APIClient

from application.factories import EventFactory


class EventNearbyIntegrationTestCases(TestCase):
    """
    Nearby events API test cases
    """

    def setUp(self):
        call_command('seed', verbosity=0)
        self.api_client = APIClient()

    def test_nearby_with_box(self):
        """Test that nearby API will return an event in the bounding box"""

        event = EventFactory(
            is_private=False,
            route_coordinates=LineString(
                (115.80070495605467, -32.00691143764981),
                (115.80070495605467, -32.00691143764981)
            ),
            starting_location=Point(115.80070495605467, -32.00691143764981)
        )

        response = self.api_client.get('/api/v1/events/nearby', coordinate_data())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'"event_id":"{event.event_id}"'.encode())

    def test_nearby_does_not_show_private_events(self):
        """Test that nearby API will return an event in the bounding box"""

        event = EventFactory(
            is_private=True,
            route_coordinates=LineString(
                (115.80070495605467, -32.00691143764981),
                (115.80070495605467, -32.00691143764981)
            ),
            starting_location=Point(115.80070495605467, -32.00691143764981)
        )

        response = self.api_client.get('/api/v1/events/nearby', coordinate_data())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

        # Make the event public, and verify that it now appears in the response
        event.is_private = False
        event.save()

        response = self.api_client.get('/api/v1/events/nearby', coordinate_data())

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data, [])

        # Delete event
        event.delete()


def coordinate_data(overrides=None):
    """
    @return: Test bounding box data
    """
    if overrides is None:
        overrides = {}
    return {**{
        'ne_lat': -31.963132845044985,
        'ne_long': 115.90266239024248,
        'sw_lat': -32.03754282918533,
        'sw_long': 115.75237441328062
    }, **overrides}
