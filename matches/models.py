from django.db import models
from casters.models import Caster
from leagues.models import Circuit
from teams.models import Team

class Match(models.Model):
    """A match between two teams."""
    
    home = models.ForeignKey(
        Team, related_name='home_matches', on_delete=models.CASCADE)

    away = models.ForeignKey(
        Team, related_name='away_matches', on_delete=models.CASCADE)

    circuit = models.ForeignKey(
        Circuit, related_name='circuit_matches', on_delete=models.CASCADE)

    start_time = models.DateTimeField(blank=True, null=True)

    primary_caster = models.ForeignKey(
        Caster, related_name='casted_matches', on_delete=models.CASCADE,
        blank=True, null=True)

    secondary_casters = models.ManyToManyField(
        Caster, related_name='cocasted_matches', blank=True, null=True)

    winner = models.ForeignKey(
        Team, related_name='won_matches', on_delete=models.CASCADE, blank=True,
        null=True
    )

    loser = models.ForeignKey(
        Team, related_name='lost_matches', on_delete=models.CASCADE, blank=True,
        null=True
    )

    home_sets_won =models.PositiveSmallIntegerField(blank=True, null=True)    
    away_sets_won =models.PositiveSmallIntegerField(blank=True, null=True)    

    vod_link = models.URLField(blank=True, null=True)

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Matches'

    def __str__(self):
        return f'{self.away.name} @ {self.home.name}'

    def end_match(self, winner):
        """Set Winner and Loser for match, then save match object."""
        teams = Team.objects.filter(
            pk__in=[self.challenger.id, self.defender.id])

        self.winner = winner
        self.loser = teams.exclude(id=self.winner.id).get()

        # Do some quick sanity checking before saving.
        if not (self.winner == self.challenger or self.winner == self.defender):
            raise ValueError(
                'Winner must be a team associated with this match.')

        if not (self.loser == self.challenger or self.loser == self.defender):
            raise ValueError(
                'Loser must be a team associated with this match.')

        self.save()
