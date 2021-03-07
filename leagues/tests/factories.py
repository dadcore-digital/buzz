from datetime import datetime, timedelta
from django.utils import timezone
import random
import factory
from factory.django import DjangoModelFactory
from leagues.models import League, Season, Circuit, Round

league_names = [
    'Second Job Gaming', 'Bowling', 'Bee', 'Bear', 'Inconvenient Gaming',
    'Friendly Fun', 'Ultimate', 'Filthy Casual', 'CASH MONEY', 'Ladder'
]

season_names = [
    'Spring', 'Summer', 'Fall', 'Winter', 'Silver', 'Platinum', 'Obsidian',
    'Gold', 'Diamond', 'Double Dimaond'
]

class LeagueFactory(DjangoModelFactory):
    """Organize Seasons of play within a League."""

    class Meta:
        model = League

    name = factory.LazyAttribute(
        lambda x: f'{random.choice(league_names)} League')


    @factory.post_generation
    def captains(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.captains.add(user)


class SeasonFactory(DjangoModelFactory):
    """A season of play within a League."""

    class Meta:
        model = Season

    name = factory.LazyAttribute(
        lambda n: f'{random.choice(season_names)} League')

    league = factory.SubFactory(LeagueFactory)
    
    is_active = True
    registration_open = True
    rosters_open = True
    max_team_members = 7

    num_regular_rounds = 6
    num_tournament_rounds = 4

    registration_start = factory.LazyAttribute(
        lambda n: timezone.now())
    registration_end = factory.LazyAttribute(
        lambda obj: obj.registration_start + timedelta(days=30))
    regular_start = factory.LazyAttribute(
        lambda obj: obj.registration_end + timedelta(days=31))
    regular_end = factory.LazyAttribute(
        lambda obj: obj.regular_start + timedelta(weeks=obj.num_regular_rounds))
    tournament_start = factory.LazyAttribute(
        lambda obj: obj.regular_end + timedelta(days=1))
    tournament_end = factory.LazyAttribute(
        lambda obj: obj.tournament_start + timedelta(weeks=obj.num_tournament_rounds
    ))

    @factory.post_generation
    def rounds(self, create, extracted, **kwargs):
        if not create:
            return

        for n in range(1, self.num_regular_rounds + 1):
            self.rounds.add(
                RoundFactory(
                    season=self,
                    round_number=n,
                    name=f'Week {n}'
                )
            )  

        for x in range(1, self.num_tournament_rounds + 1):
            round_number = self.num_regular_rounds + x
            self.rounds.add(
                RoundFactory(
                    season=self,
                    round_number=round_number,
                    name=f'Playoff Week {round_number}'
                )
            )  

class CircuitFactory(DjangoModelFactory):
    """A sub-division of teams within a Season. Often split by region & rank."""
    
    class Meta:
        model = Circuit

    season = factory.SubFactory(SeasonFactory)
    region = factory.LazyAttribute(
        lambda n: random.choice(Circuit.REGION_CHOICES)[0]
    )
    tier = factory.LazyAttribute(
        lambda n: random.choice(Circuit.REGION_CHOICES)[0])


class RoundFactory(DjangoModelFactory):
    """A period of play in which matches can take place, usually a week."""
    
    class Meta:
        model = Round

    season = factory.SubFactory(SeasonFactory)
    round_number = 1
    name = 'Week 1'