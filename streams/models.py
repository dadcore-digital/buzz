from django.db import models
from django.contrib.auth.models import User
from casters.models import Caster

class Stream(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255, blank=True, null=True)
    stream_id = models.CharField(max_length=255)
    max_viewer_count = models.SmallIntegerField(blank=True, null=True)
    thumbnail_url = models.CharField(max_length=255, blank=True, null=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    is_live = models.BooleanField(default=False)

    SERVICE_CHOICES = (
        ('TW', 'Twitch'),
        ('YT', 'Youtube'),
    )
    service = models.CharField(max_length=2, choices=SERVICE_CHOICES)

    def __str__(self):
        return f'{self.name}'

class StreamerBlacklist(models.Model):
    username = models.CharField(max_length=255)
    reason = models.CharField(max_length=255, blank=True, null=True)
