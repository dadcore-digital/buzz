from rest_framework import serializers
from matches.models import Match
from .leagues import CircuitSummarySerializer


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    
    circuit = CircuitSummarySerializer()


    class Meta:
        model = Match
        fields = [
            'home', 'away', 'circuit', 'start_time', 'primary_caster'
        ]
