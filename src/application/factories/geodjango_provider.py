# pylint:disable=no-self-use
"""
Faker provider for GeoDjango types
"""

import factory
from django.contrib.gis.geos import LineString, Point
from faker.providers import BaseProvider


class GeoDjangoProvider(BaseProvider):
    """
    Faker provider for GeoDjango types
    """

    def geo_point(self, country='AU'):
        """
        Generate a Point
        """
        faker = factory.faker.faker.Faker()
        coords = faker.local_latlng(country_code=country, coords_only=True)
        return Point(x=float(coords[1]), y=float(coords[0]), srid=4326)

    def geo_line_string(self, country='AU', num_points=10):
        """
        Generate a LineString
        """
        faker = factory.faker.faker.Faker()

        points = []
        for _ in range(num_points):
            coords = faker.local_latlng(country_code=country, coords_only=True)
            points.append(Point(x=float(coords[1]), y=float(coords[0]), srid=4326))

        return LineString(points)
