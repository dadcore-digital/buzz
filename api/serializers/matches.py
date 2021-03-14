from rest_framework import serializers
from matches.models import Game, Match, Result, Set


class MatchPlayerSerializer(serializers.ModelSerializer):
    
    class Meta:
        from players.models import Player
        model = Player

        fields = [
            'id', 'name', 'name_phonetic', 'pronouns', 'discord_username',
            'twitch_username', 'bio', 'emoji', 'avatar_url', 'modified',
            'created'
        ]

class MatchTeamSummary(serializers.ModelSerializer):
    """
    Used in multiple match endpoints.
    """
    class Meta:
        from teams.models import Team
        model = Team

        fields = [
            'id', 'name', 'is_active', 'circuit_abbrev'
        ]

#################
# Game Endpoint #
#################
class GameSerializer(serializers.ModelSerializer):
    
    winner = MatchTeamSummary()
    loser = MatchTeamSummary()

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

    winner = MatchTeamSummary()
    loser = MatchTeamSummary()

    class Meta:
        model = Set
        fields = [
            'id', 'number', 'winner', 'loser'
        ]

###################
# Result Endpoint #
###################
class ResultSerializer(serializers.ModelSerializer):
    winner = MatchTeamSummary()
    loser = MatchTeamSummary()
    sets = SetSerializer(many=True)

    status = serializers.CharField(source='get_status_display')
    
    class Meta:
        model = Result
        fields = [
            'id', 'status', 'winner', 'loser', 'sets'
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

    members = MatchPlayerSerializer(many=True, read_only=True)
    
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
    
    # Needs optimization as prefetch count in future
    sets_home = serializers.IntegerField(read_only=True)
    sets_away = serializers.IntegerField(read_only=True)
    sets_total = serializers.IntegerField(read_only=True)

    class Meta:
        model = Result
        fields = [
            'id', 'status', 'winner', 'loser', 'sets_home', 'sets_away',
            'sets_total'
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
