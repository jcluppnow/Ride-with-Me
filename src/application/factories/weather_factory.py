"""
Factory for creating weather using random data.
"""
from datetime import timezone, timedelta

import factory

from faker import Faker
from faker.providers import python

fake = Faker()
fake.add_provider(python)

class WeatherFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating weather using random data.
    """
    class Meta:
        model = 'application.Weather'

    temperature = fake.pyfloat(min_value=0, max_value=50)
    humidity = fake.pyfloat(min_value=0, max_value=100)
    precipitation = fake.pyfloat(min_value=0, max_value=100)
    wind_speed = fake.pyfloat(min_value=0, max_value=350)
    wind_direction = factory.Faker('random_int', min=0, max=360)
    coordinates = factory.Faker('geo_point')
    weather_date = factory.Faker('date_time_between', start_date='+3h', end_date='+1y',
                                      tzinfo=timezone(timedelta(hours=1)))
