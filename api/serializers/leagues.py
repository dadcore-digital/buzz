from rest_framework import serializers
from rest_framework.reverse import reverse
from leagues.models import League, Season, Circuit, Round


###################
# League Endpoint #
###################
class LeagueSeasonSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Season
        fields = [
            'id', 'is_active', 'name', 'registration_open', 'rosters_open',
            'max_team_members', 'registration_start', 'registration_end',
            'regular_start', 'regular_end', 'tournament_start',
            'tournament_end'
        ]

class LeagueSerializer(serializers.ModelSerializer):
    
    seasons = LeagueSeasonSerializer(many=True, read_only=True)
    
    class Meta:
        model = League
        fields = [
            'id', 'name', 'modified', 'created', 'seasons'
        ]

###################
# Season Endpoint #
###################
class SeasonCircuitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Circuit
        fields = [
            'id', 'region', 'tier', 'name', 'verbose_name'
        ]

class SeasonRoundSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Round
        fields = ['id', 'round_number', 'name']


class SeasonSerializer(serializers.ModelSerializer):
    
    circuits = SeasonCircuitSerializer(many=True, read_only=True)
    rounds = SeasonRoundSerializer(many=True, read_only=True)

    class Meta:
        model = Season
        fields = [
            'id', 'is_active', 'name', 'registration_open', 'rosters_open',
            'max_team_members', 'registration_start', 'registration_end',
            'regular_start', 'regular_end', 'tournament_start',
            'tournament_end', 'circuits', 'rounds'
        ]

####################
# Circuit Endpoint #
####################

class CircuitTeamPlayerSerializer(serializers.ModelSerializer):
    
    class Meta:
        from players.models import Player
        model = Player
        fields = [
            'id', 'name', 'name_phonetic', 'pronouns', 'discord_username',
            'twitch_username', 'bio', 'emoji', 'avatar_url', 'modified',
            'created', 'aliases'
        ]        

class CircuitTeamSerializer(serializers.ModelSerializer):
    
    members = CircuitTeamPlayerSerializer(many=True, read_only=True)
    class Meta:
        from teams.models import Team

        model = Team
        fields = [
            'id', 'name', 'wins', 'losses', 'members'
        ]

class CircuitSeasonSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Season
        fields = [
            'id', 'is_active', 'name', 'registration_open', 'rosters_open',
            'max_team_members', 'registration_start', 'registration_end',
            'regular_start', 'regular_end', 'tournament_start',
            'tournament_end'
        ]

class CircuitSerializer(serializers.ModelSerializer):
    
    season = CircuitSeasonSerializer(many=False, read_only=True)
    teams = CircuitTeamSerializer(many=True)

    class Meta:
        model = Circuit
        depth = 1
        fields = [
            'id', 'is_active', 'region', 'tier', 'name', 'season',
            'teams', 'verbose_name'
        ]

###################
# Round Endpoints #
###################
class RoundSerializer(serializers.ModelSerializer):
    
    matches = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Round
        fields = ['round_number', 'name', 'matches']
