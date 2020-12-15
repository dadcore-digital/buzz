from django.db import models
from leagues.models import Circuit
from players.models import Player

class AwardCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Award Categories'

    def __str__(self):
        return self.name

class Award(models.Model):
    award_category = models.ForeignKey(
        AwardCategory, related_name='awards',
        on_delete=models.deletion.CASCADE
    )
    circuit = models.ForeignKey(
        Circuit, related_name='awards', on_delete=models.deletion.CASCADE
    )
    round_number = models.PositiveSmallIntegerField(default=1)
    
    player = models.ForeignKey(
        Player, related_name='awards',
        on_delete=models.deletion.CASCADE
    )

    stats = models.ManyToManyField('Stat', related_name='category')
    

    def __str__(self):
        return f'[{self.circuit} | Week/Roundp {self.round_number} | {self.award_category.name}]:  {self.player.name}'

class StatCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Stat Categories'

    def __str__(self):
        return self.name    

class Stat(models.Model):
    stat_category = models.ForeignKey(
        StatCategory, related_name='stats',
        on_delete=models.deletion.CASCADE
    )
    total = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f'{self.total} {self.stat_category.name}'

