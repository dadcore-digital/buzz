import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User

class UserFactory(DjangoModelFactory):

    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.LazyAttribute(
        lambda u: '%s_%s@%s' %
        (u.first_name.lower(),
         u.last_name.lower(),
         'example.com')
    )
    email = factory.LazyAttribute(lambda u: u.username)

    password = 'ABC123'
