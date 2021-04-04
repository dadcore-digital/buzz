import random
from random import randint
import factory
from factory.django import DjangoModelFactory
from casters.models import Caster

class CasterFactory(DjangoModelFactory):
    
    class Meta:
        model = Caster

    player = factory.SubFactory('players.tests.factories.PlayerFactory')
    bio_link = factory.LazyAttribute(
        lambda obj: f'https://example.com/{obj.player.user.username}')

            