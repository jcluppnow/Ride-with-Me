"""
Factory for creating users using random data
"""
import factory

class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating users using random data
    """
    class Meta:
        model = 'application.CustomUser'

    email = factory.Faker('email')
    full_name = factory.Faker('name')
    profile = 'static/uploads/default.png'
    password = factory.PostGenerationMethodCall('set_password', 'password')
