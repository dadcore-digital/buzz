from rest_framework import serializers
from matches.models import Match, Result, Set
from .leagues import CircuitSummarySerializer
from .teams import TeamSummaryNoCircuitSerializer


class SetSerializer(serializers.ModelSerializer):

    winner = TeamSummaryNoCircuitSerializer()
    loser = TeamSummaryNoCircuitSerializer()

    class Meta:
        model = Set
        fields = [
            'number', 'winner', 'loser'
        ]

class ResultSerializer(serializers.ModelSerializer):
    winner = TeamSummaryNoCircuitSerializer()
    loser = TeamSummaryNoCircuitSerializer()
    sets = SetSerializer(many=True)

    status = serializers.CharField(source='get_status_display')
    
    class Meta:
        model = Result
        fields = [
            'status', 'winner', 'loser', 'sets'
        ]

class MatchSerializer(serializers.HyperlinkedModelSerializer):
    
    circuit = CircuitSummarySerializer()
    home = TeamSummaryNoCircuitSerializer()
    away = TeamSummaryNoCircuitSerializer()
    result = ResultSerializer()
    
    class Meta:
        model = Match
        fields = [
            'home', 'away', 'circuit', 'start_time', 'primary_caster', 'result'
        ]
