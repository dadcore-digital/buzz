from datetime import datetime
from django.apps import apps
from django.db import models
from django.db.models import Q
from leagues.models import Circuit
from players.models import Player


class Dynasty(models.Model):
    """
    A group of Teams, either across regions or across seasons.
    """
    name = models.CharField(blank=True, max_length=255)

    class Meta:
        verbose_name_plural = 'Dynasties'
  
    def __str__(self):
        return self.name

class Team(models.Model):
    """
    A group of Member players within a League.
    """
    name = models.CharField(blank=True, max_length=255)
    circuit = models.ForeignKey(
        Circuit, related_name='teams', on_delete=models.CASCADE)
    captain = models.ForeignKey(
        Player, related_name='captained_teams', on_delete=models.CASCADE,
        blank=True, null=True
    )

    members = models.ManyToManyField(
        Player, related_name='teams', blank=True)

    dynasty = models.ForeignKey(
        Dynasty, related_name='teams', blank=True, null=True,
        on_delete=models.SET_NULL)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def is_active(self):
        """
        Return True if season associated with this Team is marked active.
        """
        return self.circuit.season.is_active

    @property
    def can_add_members(self):
        """
        Return True if rosters for season open and not at max players on team.
        """
        if (
            self.circuit.season.rosters_open and
            self.members.count() < self.circuit.season.max_team_members
        ):
            return True
        return False

    @property
    def circuit_abbrev(self):
        """
        Return abbrevatied of circuit, such as '2W'
        """
        return f'{self.circuit.tier}{self.circuit.region}'

    @property
    def losses(self):
        return self.lost_match_results.filter().count()

    @property
    def wins(self):
        return self.won_match_results.all().count()

    def __str__(self):
        if self.captain:
            return f'{self.name} (captained by {self.captain.name})'
        else:
            return f'{self.name}'


    