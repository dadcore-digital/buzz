from django.db import models
from django.contrib.auth.models import User
from casters.models import Caster

PLATFORM_CHOICES = (
    ('ST', 'Steam'),
    ('SW', 'Nintendo Switch'),
    ('XB', 'Xbox'),
)

class Playing(models.Model):
    updated = models.DateTimeField()
    total = models.PositiveSmallIntegerField()

    platform = models.CharField(
        max_length=2, choices=PLATFORM_CHOICES, default='ST')

    OS_CHOICES = (
        ('WIN', 'Windows'),
        ('MAC', 'Mac OS'),
        ('LIN', 'Linux'),
    )
    operating_system = models.CharField(
        max_length=3, choices=OS_CHOICES, blank=True, null=True)

    ranked_total = models.PositiveSmallIntegerField(blank=True, null=True)
    quickplay_total = models.PositiveSmallIntegerField(blank=True, null=True)
    custom_total = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Playing'


    def __str__(self):
        return f'{self.updated}: {self.total}'

class Release(models.Model):
    version = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    buildid = models.PositiveSmallIntegerField()
    released_on = models.DateTimeField()
    title = models.CharField(max_length=1024, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    platform = models.CharField(
        max_length=2, choices=PLATFORM_CHOICES, default='ST')
    

