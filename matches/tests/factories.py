from datetime import datetime, timedelta
import random
from random import randrange
import factory
from factory.django import DjangoModelFactory
from django.utils.timezone import make_aware
from matches.models import Match, Result, Set, Game

class MatchFactory(DjangoModelFactory):
    """A match between two teams."""

    class Meta:
        model = Match
    
    circuit = factory.SubFactory('leagues.tests.factories.CircuitFactory')

    home = factory.SubFactory(
        'teams.tests.factories.TeamFactory',
        circuit=factory.SelfAttribute('..circuit')
    )

    away = factory.SubFactory(
        'teams.tests.factories.TeamFactory',
        circuit=factory.SelfAttribute('..circuit')
    )

    round = factory.SubFactory(
        'leagues.tests.factories.RoundFactory',
    )

    start_time = factory.LazyAttribute(
        lambda obj: obj.circuit.season.regular_start + timedelta(
            weeks=obj.round.round_number) + timedelta(days=randrange(6)) 
        )

class ResultFactory(DjangoModelFactory):
    """Winner, Loser, and statistics for a particular Match."""

    class Meta:
        model = Result

    match = factory.SubFactory(MatchFactory)   

    status = Result.COMPLETED

    winner = factory.LazyAttribute(lambda obj: obj.match.home)
    loser = factory.LazyAttribute(lambda obj: obj.match.away)
    
