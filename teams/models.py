import nanoid
from datetime import datetime
from django.apps import apps
from django.conf import settings
from django.db import models
from django.db.models import Count, Q
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

def _generate_invite_code():
    """
    Using Nano ID to generate a URL-friendly, unique invite code.

    We are using an 8-char length code, which has a 1% collision chance
    over 27 years. Assuming one invite generated an hour. We are using
    a custom library with characters that do not like similar.

    This function must live outside the class so it can be used as a default
    function to populate Team.access_code field.
    """
    return nanoid.generate(settings.NANOID_LIBRARY, size=8)

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
    invite_code = models.CharField(
        max_length=8, unique=True, blank=True, default=_generate_invite_code)

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
    def loss_count(self):
        return self.lost_match_results.filter().count()

    @property
    def win_count(self):
        return self.won_match_results.all().count()

    def generate_invite_code(self):
        """
        Using Nano ID to generate a URL-friendly, unique invite code.

        See doc string for generate_invite_code function (outside of this 
        model) for further details. 
        """
        new_invite_code = _generate_invite_code()
        self.invite_code = new_invite_code
        self.save()
        return new_invite_code

    def __str__(self):
        if self.captain:
            return f'{self.name} (captained by {self.captain.name})'
        else:
            return f'{self.name}'


    