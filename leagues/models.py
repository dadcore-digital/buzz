from django.db import models
from django.contrib.auth.models import User

ROUND_LOOKUP = {
    'Week 0': 0,
    'Week 1': 1, 
    'Week 2': 2, 
    'Week 3': 3, 
    'Week 4': 4, 
    'Week 5': 5, 
    'Week 6': 6, 
    'Week 7': 7,
    'Week 8': 8,
    'Week 9': 9,
    'Week 10': 10,            
    'Playoffs 1': 7, 
    'Playoffs 2': 8, 
    'Bye-Match': 0, 
    'Semifinals': 9, 
    'Semifinals-W1': 9.1, 
    'Semifinals-L1': 9.1, 
    'Semifinals-L2': 9.2, 
    'Championships': 10, 
    'Championships-L1': 10.1, 
    'Championships-W1': 10.2, 
    'Championships-W2': 10.3,
}


class League(models.Model):
    """Organize Teams within a League."""
    name = models.CharField(max_length=255, help_text='Name your league')
    captains = models.ManyToManyField(User, related_name='captain_of')

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Season(models.Model):
    """A season of play within a League."""
    name = models.CharField(max_length=255, help_text='Name your league')
    league = models.ForeignKey(
        League, related_name='seasons', on_delete=models.CASCADE)
    
    current_round = models.OneToOneField(
        'Round', on_delete=models.SET_NULL, null=True,
        related_name='current_round_season'
    )

    is_active = models.BooleanField(default=False, null=False)
    registration_open = models.BooleanField(default=False, null=False)
    rosters_open = models.BooleanField(default=False, null=False)
    max_team_members = models.PositiveIntegerField(default=7) 

    registration_start = models.DateTimeField(blank=True, null=True)
    registration_end = models.DateTimeField(blank=True, null=True)
    regular_start = models.DateTimeField(blank=True, null=True)
    regular_end = models.DateTimeField(blank=True, null=True)
    tournament_start = models.DateTimeField(blank=True, null=True)
    tournament_end = models.DateTimeField(blank=True, null=True)

    num_regular_rounds = models.PositiveIntegerField(default=1)
    num_tournament_rounds = models.PositiveIntegerField(default=1)

    teams_csv_url = models.URLField(blank=True, null=True)
    matches_csv_url = models.URLField(blank=True, null=True)
    awards_csv_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'{self.league.name} {self.name}'

class Circuit(models.Model):
    """A sub-division of teams within a Season. Often split by region & rank."""
    REGION_CHOICES = (
        ('W', 'West'),
        ('E', 'East'),
        ('A', 'All'),
        ('Wa', 'West A'),
        ('Wb', 'West B'),
    )

    TIER_CHOICES = (
        ('1', 'Tier 1'),
        ('2', 'Tier 2'),
        ('2A', 'Tier 2A'),
        ('2B', 'Tier 2B'),                
        ('3', 'Tier 3'),
        ('4', 'Tier 4'),        
        ('0', 'No Tier'),
    )

    season = models.ForeignKey(
        Season, related_name='circuits', on_delete=models.CASCADE)

    region = models.CharField(max_length=2, choices=REGION_CHOICES)
    tier = models.CharField(max_length=2, choices=TIER_CHOICES)
    name = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='Optionally specify a manual name for this league'
    )

    @property
    def is_active(self):
        """
        Return True if season associated with this Cricuit is marked active.
        """
        return self.season.is_active

    @property
    def verbose_name(self):
        """Full name of circuit, e.g. Tier 2 East."""
        return f'{self.get_tier_display()} {self.get_region_display()}'

    @property
    def league(self):
        return self.season.league

    def __str__(self):
        if self.name:
            return self.name
        else:
            return f'{self.league.name} {self.season.name} {self.get_region_display()} {self.get_tier_display()}'

class Group(models.Model):
    """Split up teams within a Circuit into Groups for brackets, etc."""

    circuit = models.ForeignKey(
        Circuit, related_name='groups', on_delete=models.CASCADE)

    name = models.CharField(max_length=255)

    number = models.DecimalField(
        max_digits=4, decimal_places=2, default=1.0, blank=True, null=True)

    def __str__(self):
        return f'[{self.circuit}] {self.name}'

class Round(models.Model):
    """A period of play in which matches can take place, usually a week."""
    season = models.ForeignKey(
        Season, related_name='rounds', on_delete=models.CASCADE)
    round_number = models.DecimalField(
        max_digits=4, decimal_places=2, default=1.0, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['round_number', '-name']

    @property
    def is_current_round(self):
        """Return True is this round is set as Season.current_round."""
        return hasattr(self, 'current_round_season')

    def __str__(self):
        prepend_text =  ''
        if self.name:
            prepend_text = f'{self.name} '         
        return f'{self.season} {prepend_text}Round {self.round_number}'
    