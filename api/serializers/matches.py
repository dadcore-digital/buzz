from rest_framework import serializers
from matches.models import Match
from .leagues import CircuitSummarySerializer
from .teams import TeamSummaryNoCircuitSerializer


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    
    circuit = CircuitSummarySerializer()
    home = TeamSummaryNoCircuitSerializer()
    away = TeamSummaryNoCircuitSerializer()

    class Meta:
        model = Match
        fields = [
            'home', 'away', 'circuit', 'start_time', 'primary_caster'
        ]
