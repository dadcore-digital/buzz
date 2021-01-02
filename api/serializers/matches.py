from rest_framework import serializers
from matches.models import Match, Result, Set
from .casters import CasterSummarySerializer
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
    primary_caster = CasterSummarySerializer()
    secondary_casters = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name')
    
    class Meta:
        model = Match
        fields = [
            'home', 'away', 'circuit', 'start_time', 'time_until',
            'primary_caster', 'secondary_casters', 'result'
        ]
