from rest_framework import serializers
from matches.models import Match, Result, Set
from .casters import CasterSummarySerializer
from .leagues import CircuitSummarySerializer, RoundSummarySerializer
from .teams import TeamSummaryNoCircuitSerializer, TeamSummaryBriefSerializer


class SetSerializer(serializers.ModelSerializer):

    winner = TeamSummaryBriefSerializer()
    loser = TeamSummaryBriefSerializer()

    class Meta:
        model = Set
        fields = [
            'number', 'winner', 'loser'
        ]

class ResultSerializer(serializers.ModelSerializer):
    winner = TeamSummaryBriefSerializer()
    loser = TeamSummaryBriefSerializer()
    sets = SetSerializer(many=True)

    status = serializers.CharField(source='get_status_display')
    
    class Meta:
        model = Result
        fields = [
            'status', 'winner', 'loser', 'sets', 'set_count'
        ]

class MatchSerializer(serializers.HyperlinkedModelSerializer):
    
    circuit = CircuitSummarySerializer()
    home = TeamSummaryNoCircuitSerializer()
    away = TeamSummaryNoCircuitSerializer()
    
    round = RoundSummarySerializer()

    result = ResultSerializer()
    primary_caster = CasterSummarySerializer()
    secondary_casters = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name')
    
    class Meta:
        model = Match
        fields = [
            'home', 'away', 'circuit', 'round', 'start_time', 'time_until',
            'scheduled', 'primary_caster', 'secondary_casters', 'result',
            'vod_link'
        ]
