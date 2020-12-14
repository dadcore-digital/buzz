from django.db import models, IntegrityError
from players.models import Player

class Caster(models.Model):
    """A community member who provides live game commentary."""
    player = models.OneToOneField(
        Player, related_name='caster_profile', on_delete=models.CASCADE)    
    bio_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.player.name

class Settings(models.Model):
    """Settings data for use with caster app."""
    casters_csv_url = models.URLField()

    class Meta:
        verbose_name_plural = 'settings'

    def save(self, *args, **kwargs):
        if not self.pk and Settings.objects.exists():
            raise IntegrityError('A Caster Settings object already exists.')
        
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Caster Settings'
