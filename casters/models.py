from django.db import models
from players.models import Player

class Caster(models.Model):
    """A community member who provides live game commentary."""
    player = models.OneToOneField(
        Player, related_name='caster_profile', on_delete=models.CASCADE)    
    bio_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.player.name
