from datetime import datetime
from django.apps import apps
from django.db import models
from django.db.models import Q
from leagues.models import Circuit
from players.models import Player


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

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.captain:
            return f'{self.name} (captained by {self.captain.name})'
        else:
            return f'{self.name}'

