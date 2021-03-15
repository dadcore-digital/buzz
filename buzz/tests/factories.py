from random import randint
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from allauth.socialaccount.models import SocialAccount

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

class TokenFactory(DjangoModelFactory):
    
    class Meta:
        model = User
    
    user = factory.SubFactory(UserFactory)

class SocialAccountFactory(DjangoModelFactory):
    
    class Meta:
        model = SocialAccount

    user = factory.SubFactory('buzz.tests.factories.UserFactory')
    provider = 'discord'
    uid = factory.LazyAttribute(
        lambda x: randint(100000000000000000, 999999999999999999))
    extra_data = "{}"

