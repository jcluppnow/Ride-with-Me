"""
Integration tests for the profile API
"""
import base64

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase

from rest_framework.test import APIClient

from application.models import CustomUser


class ProfileIntegrationTestCases(TestCase):
    """
    Tests for the profile model
    """

    def setUp(self):
        call_command('seed', verbosity=0)
        self.api_client = APIClient()
        self.api_client.force_login(CustomUser.objects.first())

    def test_update_profile(self):
        """Test that the profile can be successfully updated"""

        image_data = """iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI
                        12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="""

        response = self.api_client.put('/api/v1/profile', data={
            'email': 'new@example.com',
            'full_name': 'New name',
            'profile': SimpleUploadedFile(
                "image.png",
                base64.b64decode(image_data),
                content_type="image/png")
        })

        self.assertEqual(response.status_code, 200)
