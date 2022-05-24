"""
Factory for creating events using random data
"""
from datetime import timezone, timedelta

import factory

from faker import Faker
from faker.providers import python
from .user_factory import UserFactory
from .weather_factory import WeatherFactory
from .geodjango_provider import GeoDjangoProvider

fake = Faker()
fake.add_provider(python)

class EventFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating events using random data
    """

    factory.Faker.add_provider(GeoDjangoProvider)

    class Meta:
        model = 'application.Event'

    average_speed = factory.Faker('random_int', min=5, max=50)
    # Faker must be resolved now because we are using GeoDjango LineString,
    # use faker library itself rather than factory boy's instance
    route_coordinates = factory.Faker('geo_line_string')
    name = factory.Faker('sentence', nb_words=3)
    max_participants = factory.Faker('random_int', min=5, max=50)
    description = factory.Faker('text')
    starting_time = factory.Faker('date_time_between', start_date='+3h', end_date='+1y',
                                  tzinfo=timezone(timedelta(hours=1)))
    is_private = factory.Faker('boolean', chance_of_getting_true=25)
    starting_location = factory.Faker('geo_point')
    hero_image = "/uploads/hero_images/default.png"
    # Must override username to use this instance of factory - bug with factory boy
    organiser = factory.SubFactory(UserFactory)
    weather = factory.SubFactory(WeatherFactory)

    @factory.post_generation
    def participants(self, create, extracted, **kwargs):
        """
        Adds participants to the event if they are passed in
        [e.g. EventFactory.create(participants=(user1, user2, user3))]
        """
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # Extracted represents the list of participants
            for participant in extracted:
                self.participants.add(participant)  # pylint: disable=no-member
