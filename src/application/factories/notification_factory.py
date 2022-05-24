"""
Factory for creating notifications using random data
"""
import factory

from faker import Faker
from faker.providers import python

from .event_factory import EventFactory
from .user_factory import UserFactory

fake = Faker()
fake.add_provider(python)


class NotificationFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating notifications using random data
    """

    class Meta:
        model = 'application.Notification'

    notifier = factory.SubFactory(UserFactory)
    content = factory.Faker('sentence')
    event = factory.SubFactory(EventFactory)
    recipient = factory.SubFactory(UserFactory)
