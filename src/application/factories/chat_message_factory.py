"""
Factory for creating chat messages with random data
"""

import factory

from .user_factory import UserFactory
from .event_factory import EventFactory

class ChatMessageFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating chat messages with random data
    """

    class Meta:
        model = 'application.ChatMessage'

    sender = factory.SubFactory(UserFactory)
    content = factory.Faker('sentence')
    event = factory.SubFactory(EventFactory)

    @factory.post_generation
    def add_sender_to_event(self, create, extracted, **kwargs): # pylint:disable=unused-argument
        """
        Adds sender to the event
        """
        if create:
            self.event.participants.add(self.sender)
