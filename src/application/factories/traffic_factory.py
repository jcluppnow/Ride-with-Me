"""
Factory for creating traffic data using random data.
"""
from datetime import timezone, timedelta

import factory

from faker import Faker
from .geodjango_provider import GeoDjangoProvider

fake = Faker()

class TrafficFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating traffic data using random data.
    """

    factory.Faker.add_provider(GeoDjangoProvider)

    class Meta:
        model = 'application.Traffic'

    description = factory.Faker('text')
    start_date = factory.Faker('date_time_between', start_date='+3h', end_date='+1y',
                                  tzinfo=timezone(timedelta(hours=1)))
    end_date = factory.Faker('date_time_between', start_date='+3h', end_date='+1y',
                                  tzinfo=timezone(timedelta(hours=1)))
    last_updated = factory.Faker('date_time_between', start_date='+3h', end_date='+1y',
                                  tzinfo=timezone(timedelta(hours=1)))
    road_closed = factory.Faker('boolean', chance_of_getting_true=50)
    severity = factory.Faker('random_int', min=1, max=4)
    traffic_type = factory.Faker('random_int', min=1, max=11)
    verified = factory.Faker('boolean', chance_of_getting_true=50)
    coordinates = factory.Faker('geo_point')
