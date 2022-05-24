"""
Integration tests for the event API
"""
import base64

from django.test import TestCase
from django.core.management import call_command
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APIClient

from application.models import CustomUser


class EventCreateIntegrationTestCases(TestCase):
    """
    Tests for the event model
    """

    def setUp(self):
        call_command('seed', verbosity=0)
        self.api_client = APIClient()
        self.api_client.force_login(CustomUser.objects.first())

    def test_create_event(self):
        """Test sending valid data creates an event"""

        response = self.api_client.post('/api/v1/events/', event_data())

        self.assertEqual(response.status_code, 201)

    def test_create_event_route_coordinates_point_validation(self):
        """Test validation fails if route_coordinates is a point"""

        response = self.api_client.post('/api/v1/events/', data=event_data({
            'route_coordinates': """{
              'type': 'Point',
              'coordinates': [
                [
                  -0.057334899902344,
                  0.05081176091777
                ]
              ]
            }"""
        }))

        self.assertEqual(response.status_code, 400)

    def test_create_event_route_coordinates_single_coordinate_validation(self):
        """Test validation fails if route_coordinates has a single coordinate"""

        response = self.api_client.post('/api/v1/events/', data=event_data({
            'route_coordinates': """{
              'type': 'LineString',
              'coordinates': [
                [
                  -0.057334899902344,
                  0.05081176091777
                ]
              ]
            }"""
        }))

        self.assertEqual(response.status_code, 400)

    def test_create_event_average_speed_validation(self):
        """Test that validation fails if the average speed is zero"""

        response = self.api_client.post('/api/v1/events/', data=event_data({
            'average_speed': 0
        }))

        self.assertEqual(response.status_code, 400)

    def test_create_event_max_participants_zero_validation(self):
        """Test that validation fails if the max participants is zero"""

        response = self.api_client.post('/api/v1/events/', data=event_data({
            'max_participants': 0
        }))

        self.assertEqual(response.status_code, 400)

    def test_create_event_max_participants_negative_validation(self):
        """Test that validation fails if the max participants is negative"""

        response = self.api_client.post('/api/v1/events/', data=event_data({
            'max_participants': -1
        }))

        self.assertEqual(response.status_code, 400)

    def test_create_event_name_empty_validation(self):
        """Test that validation fails if the event name is empty"""

        response = self.api_client.post('/api/v1/events/', data=event_data({
            'name': ''
        }))

        self.assertEqual(response.status_code, 400)


def event_data(overrides=None):
    """
    @return: Test event data
    """
    if overrides is None:
        overrides = {}
    image_data = """iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI
                    12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="""

    return {**{
        'average_speed': 20,
        'route_coordinates': """{
        'type': 'LineString',
        'coordinates': [
          [
            -0.057334899902344,
            0.05081176091777
          ],
          [
            0.066261291503906,
            0.049095147800738
          ],
          [
            0.048408508300781,
            -0.005493164054107
          ],
          [
            -0.048408508300781,
            -0.018196105651185
          ],
          [
            -0.057334899902344,
            0.017166137438487
          ],
          [
            -0.0933837890625,
            -0.028152464687518
          ],
          [
            -0.055120916716347,
            -0.356446295495548
          ],
          [
            0.044975280761719,
            -0.04943847042774
          ]
        ]
      }""",
        'name': 'Event',
        'max_participants': 10,
        'description': 'Description for event',
        'starting_time': '2022-01-20T04:52:00Z',
        'is_private': False,
        'starting_location': """{
        'type': 'Point',
        'coordinates': [
          115.82,
          -31.9635701708822
        ]
      }""",
        'hero_image': SimpleUploadedFile(
            "image.png",
            base64.b64decode(image_data),
            content_type="image/png"
        )
    }, **overrides}
