from django.db import models
from django.db.models import Count, Case, When, IntegerField
from django.contrib.auth.models import User

class Player(models.Model):
    name = models.CharField(unique=True, max_length=255)
    name_phonetic = models.CharField(max_length=255, blank=True, null=True)
    pronouns = models.CharField(max_length=255, blank=True, null=True)

    discord_username = models.CharField(blank=True, null=True, max_length=255)
    twitch_username = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(
        User, related_name='captained_teams', on_delete=models.CASCADE,
        blank=True, null=True
    )
    
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.discord_username:
            return f'{self.name} (@{self.discord_username})'
        else:
            return self.name

    @property
    def award_summary(self):
        from awards.models import AwardCategory

        categories = AwardCategory.objects.filter(
            awards__player__name=self.name).distinct()
        
        awards = []
        
        for category in categories:
            awards.append({
                'name': category.name,
                'discord_emoji': category.discord_emoji,
                'count': self.awards.filter(award_category=category).count()
            })
        
        return awards


class Alias(models.Model):
    name = models.CharField(unique=True, max_length=255)
    is_primary = models.BooleanField(default=False)
    player = models.ForeignKey(
        Player, related_name='aliases', on_delete=models.CASCADE)

    verbose_name_plural = 'Aliases'

    def __str__(self):
        alias_type = 'secondary'
        
        if self.is_primary:
            alias_type = 'primary'

        return f'{self.name} {alias_type} alias of {self.player.name}'

class PlayerSettings(models.Model):
    """
    Global settings related to players.
    """
    players_csv_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Settings'