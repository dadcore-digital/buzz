from django.db import models
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


class Alias(models.Model):
    name = models.CharField(unique=True, max_length=255)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
