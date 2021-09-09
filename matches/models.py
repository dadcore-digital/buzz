import arrow
import datetime
from django.db import models
from django.urls import reverse
from buzz.services import trim_humanize
from casters.models import Caster
from leagues.models import Circuit, Group, Round
from players.models import Player
from teams.models import Team
from matches.managers import ResultManager, SetManager


class Match(models.Model):
    """A match between two teams."""
    
    home = models.ForeignKey(
        Team, related_name='home_matches', on_delete=models.CASCADE)

    away = models.ForeignKey(
        Team, related_name='away_matches', blank=True, null=True,
        on_delete=models.CASCADE
    )

    circuit = models.ForeignKey(
        Circuit, related_name='circuit_matches', on_delete=models.CASCADE)

    group = models.ForeignKey(
        Group, related_name='group_matches', on_delete=models.SET_NULL,
        blank=True, null=True)

    round = models.ForeignKey(
        Round, related_name='matches', on_delete=models.CASCADE)

    start_time = models.DateTimeField(blank=True, null=True)

    primary_caster = models.ForeignKey(
        Caster, related_name='casted_matches', on_delete=models.SET_NULL,
        blank=True, null=True)

    secondary_casters = models.ManyToManyField(
        Caster, related_name='cocasted_matches', blank=True, null=True)

    vod_link = models.URLField(blank=True, null=True)

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Matches'

    @property
    def circuit_display(self):
        if self.home:
            if self.home.group and self.circuit:
                return f'{self.circuit.name} - {self.home.group.name}'

        if self.circuit:
            return self.circuit.name
        
        return ''

    @property
    def time_until(self):
        if self.start_time:
            arrow_start_time = arrow.get(self.start_time)
            humanized_start = arrow_start_time.humanize(
                granularity=['week', 'day', 'hour', 'minute'])

            return trim_humanize(humanized_start)
        return self.start_time

    @property
    def scheduled(self):
        if self.start_time:
            return True
        return False
        
    def __str__(self):
        if self.away:
            return f'{self.away.name} @ {self.home.name}'
        else:
            return f'Nobody @ {self.home.name}'

    def get_absolute_url(self):
        return reverse('match-detail', kwargs={'pk': self.pk})

class Result(models.Model):
    """Winner, Loser, and statistics for a particular Match."""

    match = models.OneToOneField(
        Match, related_name='result', on_delete=models.CASCADE, blank=True,
        null=True)    

    created_by = models.ForeignKey(
        Player, blank=True, null=True, on_delete=models.deletion.SET_NULL,
        related_name='created_results'
    )

    COMPLETED = 'C'
    SINGLE_FORFEIT = 'SF'
    DOUBLE_FORFEIT = 'DF'
    BYE = 'BY'
    
    STATUS_CHOICES = (
        (COMPLETED, 'Completed'),
        (SINGLE_FORFEIT, 'Single Forfeit'),
        (DOUBLE_FORFEIT, 'Double Forfeit'),
        (BYE, 'Bye'),
    )

    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES)

    UPLOADER = 'UL'
    SHEETS = 'SH'
    ADMIN = 'AM'
    
    SOURCE_CHOICES = (
        (UPLOADER, 'Match Uploader'),
        (SHEETS, 'Google Sheets'),
        (ADMIN, 'Buzz Admin')
    )

    source = models.CharField(
        max_length=2, choices=SOURCE_CHOICES, blank=True, null=True)

    winner = models.ForeignKey(
        Team, related_name='won_match_results', on_delete=models.CASCADE,
        blank=True, null=True
    )

    loser = models.ForeignKey(
        Team, related_name='lost_match_results', on_delete=models.CASCADE,
        blank=True, null=True)

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    notes = models.CharField(max_length=1024, blank=True, null=True)

    objects = ResultManager()


    def __str__(self):
        if self.loser:
            return f'{self.winner.name} over {self.loser.name} in {self.sets.count()} sets'
        elif self.winner:
            return f'{self.winner.name} over Nobody '
        else:
            return 'Nobody over Nobody (DF)'

    @property
    def set_count(self):
        if self.sets.all():
            return {
                'home': self.sets.filter(winner=self.match.home).count(),
                'away': self.sets.filter(winner=self.match.away).count(),
                'total': self.sets.all().count()
            }
            
        return None
    

class Set(models.Model):
    """A series of games played in a Match."""
    result = models.ForeignKey(
        Result, related_name='sets', on_delete=models.CASCADE, blank=True,
        null=True)

    number = models.PositiveSmallIntegerField(default=1)

    winner = models.ForeignKey(
        Team, related_name='won_sets', on_delete=models.CASCADE)

    loser = models.ForeignKey(
        Team, related_name='lost_sets', on_delete=models.CASCADE)

    objects = SetManager()

    def __str__(self):
        return f'Set {self.number}: {self.winner.name}'

    def generate_games(self):
        """Create Game objects via JSON objects associated with this set."""
        if hasattr(self, 'log'):
            
            try:
                # Delete any old games, no dupes!
                if self.games.exists():
                    self.games.all().delete()
            
                WINCON_LOOKUP = {1: 'M', 2: 'E', 3: 'S'}
                MAP_LOOKUP = {
                    2: 'PD', 4: 'BQ', 7: 'HT', 11:'TF', 14: 'SP', 15: 'SJ',
                    17: 'NF', 18: 'TR'
                }

                blue_team = self.result.team_mappings.filter(
                    color=2).first().team
                
                gold_team = self.result.team_mappings.filter(
                    color=1).first().team

                TEAM_LOOKUP = {1: gold_team, 2: blue_team}

                log = self.log.body
                log_games = log['games']

                for idx, entry in enumerate(log_games):
                    game = Game()
                    game.number = idx + 1
                    game.win_condition = WINCON_LOOKUP[entry['winCondition']]
                    game.winner = TEAM_LOOKUP[log['gameWinners'][idx]]
                    game.loser = blue_team if game.winner == gold_team else gold_team
                    game.duration = datetime.timedelta(seconds=entry['duration'])
                    game.map = MAP_LOOKUP[log['mapPool'][idx]]
                    game.save()
                    self.games.add(game)
            
            # Malformed JSON File
            except AttributeError:
                pass

class SetLog(models.Model):
    """Log data for a set, should be a single JSONField."""
    set = models.OneToOneField(
        Set, related_name='log', on_delete=models.CASCADE
    )

    filename = models.CharField(max_length=255, blank=True, null=True)
    body = models.JSONField()

    def __str__(self):
        return f'Log Data for {self.set}'

class Game(models.Model):
    """A single map played in a Set."""
    number = models.PositiveSmallIntegerField(default=1)

    MAP_CHOICES = (
        ('PD', 'The Pod'),
        ('TF', 'The Tally Fields'),
        ('NF', 'The Nesting Flats'),
        ('SJ', 'Split Juniper'),
        ('BQ', 'Black Queen\'s Keep'),
        ('HT', 'Helix Temple'),
        ('SP', 'The Spire'),
        ('TR', 'The Throne Room')
    )

    map = models.CharField(
        max_length=2, choices=MAP_CHOICES, blank=True, null=True)

    winner = models.ForeignKey(
        Team, related_name='won_games', on_delete=models.CASCADE, blank=True,
        null=True)

    loser = models.ForeignKey(
        Team, related_name='lost_games', on_delete=models.CASCADE, blank=True,
        null=True)

    set = models.ForeignKey(
        Set, related_name='games', on_delete=models.CASCADE, blank=True,
        null=True
    )
    

    WIN_CONDITION_CHOICES = (
        ('E', 'Economic'),
        ('M', 'Military'),
        ('S', 'Snail')
    )

    win_condition = models.CharField(
        max_length=1, choices=WIN_CONDITION_CHOICES, blank=True, null=True)

    duration = models.DurationField(blank=True, null=True)

    def __str__(self):
        return f'Game {self.number}: {self.winner.name}'


class PlayerMapping(models.Model):

    result = models.ForeignKey(
        Result, related_name='player_mappings', on_delete=models.CASCADE, blank=True,
        null=True)

    nickname = models.CharField(max_length=255)
    player = models.ForeignKey(
        Player, related_name='player_mapping', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Player Mappings'

    def __str__(self):
        return f'{self.nickname} --> {self.player.name}'

class TeamMapping(models.Model):

    result = models.ForeignKey(
        Result, related_name='team_mappings', on_delete=models.CASCADE, blank=True,
        null=True)
    
    GOLD = 1
    BLUE = 2

    COLOR_CHOICES = (
        (BLUE, 'Blue'),
        (GOLD, 'Gold')
    )

    color = models.IntegerField(max_length=1, choices=COLOR_CHOICES)
    team = models.ForeignKey(
        Team, related_name='team_mapping', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Team Mappings'

    def __str__(self):
        return f'{self.color} --> {self.team.name}'