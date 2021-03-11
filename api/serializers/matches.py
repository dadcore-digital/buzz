from rest_framework import serializers
from matches.models import Game, Match, Result, Set
from .teams import TeamSummaryNoCircuitSerializer, TeamSummaryBriefSerializer


#################
# Game Endpoint #
#################
class GameSerializer(serializers.ModelSerializer):
    
    winner = TeamSummaryBriefSerializer()
    loser = TeamSummaryBriefSerializer()

    class Meta:
        model = Game
        fields = [
            'id', 'number', 'winner', 'loser', 'home_berries', 'away_berries',
            'home_smail', 'away_snail', 'home_queen_deaths',
            'away_queen_deaths', 'win_condition'
        ]

################
# Set Endpoint #
################
class SetSerializer(serializers.ModelSerializer):

    winner = TeamSummaryBriefSerializer()
    loser = TeamSummaryBriefSerializer()

    class Meta:
        model = Set
        fields = [
            'id', 'number', 'winner', 'loser'
        ]

###################
# Result Endpoint #
###################
class ResultSerializer(serializers.ModelSerializer):
    winner = TeamSummaryBriefSerializer()
    loser = TeamSummaryBriefSerializer()
    sets = SetSerializer(many=True)

    status = serializers.CharField(source='get_status_display')
    
    class Meta:
        model = Result
        fields = [
            'id', 'status', 'winner', 'loser', 'sets', 'set_count'
        ]

##################
# Match Endpoint #
##################
class MatchCircuitSeasonSerializer(serializers.ModelSerializer):
    
    class Meta:
        from leagues.models import Season
        model = Season
        fields = ['id', 'name', ]

class MatchCircuitSerializer(serializers.ModelSerializer):
    season = MatchCircuitSeasonSerializer(many=False, read_only=True)

    class Meta:
        from leagues.models import Circuit
        model = Circuit
        fields = ['id', 'season', 'region', 'tier', 'name', 'verbose_name']

class MatchRoundSummarySerializer(serializers.ModelSerializer):
    
    number = serializers.DecimalField(
        source='round_number', max_digits=4, decimal_places=2)

    class Meta:
        from leagues.models import Round
        model = Round
        fields = ['number', 'name']

class MatchTeamSerializer(serializers.ModelSerializer):

    members = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name')
    
    class Meta:
        from teams.models import Team
        model = Team
        fields = [
            'id', 'name', 'members'            
        ]

class MatchCasterSummarySerializer(serializers.ModelSerializer):
    
    class Meta:
        from casters.models import Caster
        model = Caster
        fields = [
            'name', 'bio_link', 'stream_link'
        ]

class MatchResultSerializer(serializers.ModelSerializer):

    winner = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field='name')
    loser = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field='name')

    status = serializers.CharField(source='get_status_display')
    
    class Meta:
        model = Result
        fields = [
            'id', 'status', 'winner', 'loser', 'set_count'
        ]

class MatchSerializer(serializers.ModelSerializer):
    
    circuit = MatchCircuitSerializer()
    home = MatchTeamSerializer()
    away = MatchTeamSerializer()
    round = MatchRoundSummarySerializer()
    result = MatchResultSerializer()

    primary_caster = MatchCasterSummarySerializer()
    secondary_casters = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name')
    
    class Meta:
        model = Match
        fields = [
            'id', 'home', 'away', 'circuit', 'round', 'start_time',
            'time_until', 'scheduled', 'primary_caster', 'secondary_casters',
            'result', 'vod_link'
        ]
