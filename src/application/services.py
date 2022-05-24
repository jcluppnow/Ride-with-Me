"""
Contains services for the application
"""

from django.conf import settings
import reverse_geocoder as rg
from .mocks import MockReverseGeocoder


class ReverseGeocoder(): # pylint: disable=too-few-public-methods
    """ReverseGeocoder service that converts coordinates to a location."""

    def __init__(self):
        """
        Intialise reverse geocoder service
        """
        if settings.ENV == 'testing':
            self.rg_service = MockReverseGeocoder
        else:
            self.rg_service = rg

    def search(self, coordinates):
        """
        Return search result for given coordinates
        """
        return self.rg_service.search(coordinates)
