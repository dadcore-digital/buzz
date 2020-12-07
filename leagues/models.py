from django.db import models
from django.contrib.auth.models import User


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

    regular_start = models.DateTimeField(blank=True, null=True)
    regular_end = models.DateTimeField(blank=True, null=True)
    playoffs_start = models.DateTimeField(blank=True, null=True)
    playoffs_end = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

class Circuit(models.Model):
    """A sub-division of teams within a Season. Often split by region & rank."""
    REGION_CHOICES = (
        ('W', 'West'),
        ('E', 'East'),
        ('A', 'All')
    )

    TIER_CHOICES = (
        ('1', 'Tier 1'),
        ('2', 'Tier 2'),
        ('3', 'Tier 3'),
        ('0', 'No Tier'),
    )

    season = models.ForeignKey(
        Season, related_name='circuits', on_delete=models.CASCADE)

    region = models.CharField(max_length=1, choices=REGION_CHOICES)
    tier = models.CharField(max_length=1, choices=TIER_CHOICES)
    name = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='Optionally specify a manual name for this league'
    )

    @property
    def league(self):
        return self.season.league

    def __str__(self):
        if self.name:
            return self.name
        else:
            return f'{self.league.name} {self.season.name} {self.get_region_display()} {self.get_tier_display()}'
