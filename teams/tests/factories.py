import random
from random import randrange
import factory
import faker
from factory.django import DjangoModelFactory
from teams.models import Dynasty, Team

fake = faker.Faker()

class DynastyFactory(DjangoModelFactory):
    """
    A group of Teams, either across regions or across seasons.
    """
    class Meta:
        model = Dynasty
    
    name = factory.LazyAttribute(
        lambda n: f'{fake.bs().title()} Dynasty'
    )

class TeamFactory(DjangoModelFactory):
    """
    A group of Member players within a League.
    """
    class Meta:
        model = Team

    name = factory.LazyAttribute(
        lambda n: ' '.join(fake.words(randrange(2, 7))).title()
    )

    circuit = factory.SubFactory('leagues.tests.factories.CircuitFactory')
    captain = factory.SubFactory('players.tests.factories.PlayerFactory')

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for member in extracted:
                self.members.add(member)
