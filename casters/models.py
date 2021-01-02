from django.db import models, IntegrityError
from players.models import Player

class Caster(models.Model):
    """A community member who provides live game commentary."""
    player = models.OneToOneField(
        Player, related_name='caster_profile', on_delete=models.CASCADE)    
    bio_link = models.URLField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    does_solo_casts = models.BooleanField(default=True)
    
    @property
    def stream_link(self):
        if self.player:
            if self.player.twitch_username:
                return f'https://twitch.tv/{self.player.twitch_username}'
        
        return ''
                
    @property
    def name(self):
        return self.player.name

    def __str__(self):
        return self.player.name

class NameMapping(models.Model):
    """
    Manually map the name of a caster to a player

    Useful when a caster plays with a different name than their casting name.
    """
    caster_name = models.CharField(max_length=255)
    player_name = models.CharField(max_length=255)

    def __str__(self):
        return f'"{self.caster_name}" plays as "{self.player_name}"'


class Settings(models.Model):
    """Settings data for use with caster app."""
    casters_csv_url = models.URLField()

    # A list of names to ignore when importing, seperated by comma
    ignore_names = models.CharField(blank=True, null=True, max_length=255)

    class Meta:
        verbose_name_plural = 'settings'

    def save(self, *args, **kwargs):
        if not self.pk and Settings.objects.exists():
            raise IntegrityError('A Caster Settings object already exists.')
        
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Caster Settings'
