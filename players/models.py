from django.db import models
from django.db.models import Count, Case, When, IntegerField
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Player(models.Model):
    name = models.CharField(unique=True, max_length=255)
    user = models.OneToOneField(
        User, related_name='player', on_delete=models.SET_NULL,
        blank=True, null=True
    )

    name_phonetic = models.CharField(max_length=255, blank=True, null=True)
    pronouns = models.CharField(max_length=255, blank=True, null=True)

    discord_username = models.CharField(blank=True, null=True, max_length=255)
    avatar_url = models.URLField(blank=True, null=True)

    twitch_username = models.CharField(blank=True, null=True, max_length=255)

    bio = models.CharField(blank=True, null=True, max_length=1000)
    emoji = models.CharField(blank=True, null=True, max_length=32)
    
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

    @property
    def discord_avatar_url(self):
        """Retrieve a URL to a player's Discord avatar, given a Player object."""    
        user = self.user
        social_account = user.socialaccount_set.all().first()

        if social_account:
            uid = social_account.extra_data['id']
            avatar = social_account.extra_data['avatar']
            return f'https://cdn.discordapp.com/avatars/{uid}/{avatar}.png'

        return None

    @property
    def discord_login_username(self):
        """
        Retrieve latest discord username as recorded by Discord Login.
        """
        try:
            discord_account = self.user.socialaccount_set.all().filter(
                provider='discord').first()

            if discord_account:
                try:
                    return f"{discord_account.extra_data['username']}#{discord_account.extra_data['discriminator']}"
                except KeyError:
                    pass

        
        except AttributeError:
            pass
        
        return ''

    def get_or_create_token(self):
        """
        Return DRF auth token. Create if not present.
        """
        if self.user:
            return Token.objects.get_or_create(user=self.user)[0]
        return None

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

class IGLPlayerLookup(models.Model):
    discord_uid = models.CharField(max_length=255)
    discord_username = models.CharField(max_length=255)
    discord_nick = models.CharField(max_length=255, blank=True, null=True)
    discord_avatar_url = models.URLField(blank=True, null=True)
    igl_player_name = models.CharField(max_length=255, blank=True, null=True)

