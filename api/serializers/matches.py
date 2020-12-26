from rest_framework import serializers
from matches.models import Match


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Match
        fields = [
            'home', 'away', 'circuit', 'start_time', 'primary_caster'
        ]
