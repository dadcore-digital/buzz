from django.db import models
from django.contrib.auth.models import User
from players.models import Player

class Event(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    duration = models.DurationField(blank=True, null=True)
    description = models.CharField(max_length=5120, blank=True, null=True)

    organizers = models.ManyToManyField(
        Player, related_name='events_organized', blank=True, null=True)
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} @ {self.start_time}'

class EventLink(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    event = models.ForeignKey(
        Event, related_name='links', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} for {self.event.name}'
