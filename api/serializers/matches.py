from rest_framework import serializers
from casters.models import Caster
from matches.models import (
    Game, Match, Result, Set, SetLog, PlayerMapping, TeamMapping)
from matches.permissions import can_create_match, can_create_result
from teams.models import Team

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
            'id', 'number', 'map', 'winner', 'loser', 'win_condition', 'set',
            'duration'
        ]

################
# Set Endpoint #
################
class SetGameSerializer(serializers.ModelSerializer):
    
    winner = MatchTeamSummary()
    loser = MatchTeamSummary()

    class Meta:
        model = Game
        fields = [
            'id', 'number', 'map', 'winner', 'loser', 'win_condition',
            'duration'
        ]


class SetSerializer(serializers.ModelSerializer):

    games = SetGameSerializer(many=True, read_only=True)

    class Meta:
        model = Set
        fields = [
            'id', 'number', 'winner', 'loser', 'games', 'log'
        ]

class SetDetailLogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SetLog
        fields = [
            'id', 'filename', 'body'
        ]

class SetDetailSerializer(serializers.ModelSerializer):
    
    winner = MatchTeamSummary()
    loser = MatchTeamSummary()
    log = SetDetailLogSerializer()

    class Meta:
        model = Set
        fields = [
            'id', 'number', 'winner', 'loser', 'log'
        ]

###################
# Result Endpoint #
###################
################
class ResultSetLogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SetLog
        fields = [
            'id', 'filename', 'body'
        ]

class ResultSetGameSerializer(serializers.ModelSerializer):
    
    winner = MatchTeamSummary()
    loser = MatchTeamSummary()

    class Meta:
        model = Game
        fields = [
            'id', 'number', 'map', 'winner', 'loser', 'win_condition',
            'duration'
        ]

class ResultSetSerializer(serializers.ModelSerializer):

    winner = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False,
        queryset=Team.objects.all(),
        style={'base_template': 'input.html'}
    )

    loser = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False,
        queryset=Team.objects.all(),
        style={'base_template': 'input.html'}
    )

    games = ResultSetGameSerializer(many=True, read_only=True)

    log = ResultSetLogSerializer(required=False, write_only=True)

    class Meta:
        model = Set
        fields = [
            'id', 'number', 'winner', 'loser', 'games', 'log'
        ]

class ResultPlayerMappingSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayerMapping
        fields = ['id', 'nickname', 'player']    

class ResultTeamMappingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TeamMapping
        fields = ['id', 'color', 'team']    

class ResultSerializer(serializers.ModelSerializer):

    winner = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False,
        queryset=Team.objects.all(),
        style={'base_template': 'input.html'}
    )

    loser = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False,
        queryset=Team.objects.all(),
        style={'base_template': 'input.html'}
    )

    sets = ResultSetSerializer(many=True)

    match = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False,
        queryset=Match.objects.filter(
            circuit__season__is_active=True, result__isnull=True
        ),
        style={'base_template': 'input.html'},
    )
    
    player_mappings = ResultPlayerMappingSerializer(many=True, required=False)
    team_mappings = ResultTeamMappingSerializer(many=True, required=False)

    def create(self, validated_data):
        sets_data = validated_data.pop('sets')
                        
        player_mappings_data = []
        if 'player_mappings' in validated_data:
            player_mappings_data = validated_data.pop('player_mappings')

        team_mappings_data = []
        if 'team_mappings' in validated_data:
            team_mappings_data = validated_data.pop('team_mappings')

        result = Result.objects.create(**validated_data)

        for data in player_mappings_data:
            PlayerMapping.objects.create(result=result, **data)
        
        for data in team_mappings_data:
            TeamMapping.objects.create(result=result, **data)
        
        for data in sets_data:
            
            log_data = None
            if 'log' in data.keys():
                log_data = data.pop('log')    
            
            set = Set.objects.create(result=result, **data)
            
            if log_data:
                SetLog.objects.create(set=set, **log_data)
                set.generate_games()
    
        return result
    
    def validate(self, data):
        """
        In order for Result/Set data to be valid, they must:

        - Result winner & loser must be same as teams associated with Match
        - Set winner & loser must be same as teams associated with Match
        """
        teams = [data['match'].home, data['match'].away]
        user = self.context['request'].user

        has_permission, error = can_create_result(
            data['match'], user, return_error_msg=True)

        if not has_permission:
            raise serializers.ValidationError(error)

        if (
            data['winner'] not in teams or
            data['loser'] not in teams
        ): 
             raise serializers.ValidationError(
                 'Validation Error: Result Winner and Loser must be associated with Match')

        if len(data['sets']) < 1:
             raise serializers.ValidationError(
                 'Validation Error: You must include results for at least one Set.')

        if len(data['sets']) > 9:
             raise serializers.ValidationError(
                 'Validation Error: You cannot include more than nine Sets.')

        for set in data['sets']:
            if (
                set['winner'] not in teams or
                set['loser'] not in teams
            ): 
                raise serializers.ValidationError(
                    'Validation Error: Set Winner and Loser must be associated with Match')

        return data

    class Meta:
        model = Result
        fields = [
            'id', 'created_by', 'match', 'status', 'winner', 'loser', 'sets',
            'source', 'notes', 'player_mappings', 'team_mappings' 
        ]


class ResultDetailSetGameSerializer(serializers.ModelSerializer):
    
    winner = MatchTeamSummary()
    loser = MatchTeamSummary()

    class Meta:
        model = Game
        fields = [
            'id', 'number', 'map', 'winner', 'loser', 'win_condition',
            'duration'
        ]

class ResultDetailSetSerializer(serializers.ModelSerializer):
    
    winner = serializers.PrimaryKeyRelatedField(read_only=True)
    loser = serializers.PrimaryKeyRelatedField(read_only=True)

    games = ResultDetailSetGameSerializer(many=True, read_only=True)
    log = ResultSetLogSerializer(read_only=True)

    class Meta:
        model = Set
        fields = [
            'id', 'number', 'winner', 'loser', 'games', 'log'
        ]

class ResultDetailPlayerMappingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PlayerMapping
        fields = ['id', 'nickname', 'player']    

class ResultDetailTeamMappingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TeamMapping
        fields = ['id', 'color', 'team']

class ResultDetailSerializer(serializers.ModelSerializer):
    
    winner = serializers.PrimaryKeyRelatedField(read_only=True)
    loser = serializers.PrimaryKeyRelatedField(read_only=True)
    sets = ResultDetailSetSerializer(many=True)
    status = serializers.CharField()
    player_mappings = ResultDetailPlayerMappingSerializer(many=True)
    team_mappings = ResultDetailTeamMappingSerializer(many=True)

    
    class Meta:
        model = Result
        fields = [
            'id', 'created_by', 'match', 'status', 'winner', 'loser', 'sets',
            'source', 'notes', 'player_mappings', 'team_mappings'
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
        fields = ['number', 'name', 'is_current_round']

class MatchGroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        from leagues.models import Group
        model = Group
        fields = ['id', 'name', 'number']

class MatchTeamSerializer(serializers.ModelSerializer):

    members = MatchPlayerSerializer(many=True, read_only=True)
    group = MatchGroupSerializer(read_only=True)
    wins = serializers.IntegerField(read_only=True)
    losses = serializers.IntegerField(read_only=True)

    class Meta:
        from teams.models import Team
        model = Team
        fields = [
            'id', 'name', 'abbreviation', 'emoji', 'members', 'group', 'wins', 'losses'
        ]

class MatchCasterSummarySerializer(serializers.ModelSerializer):
    
    class Meta:
        from casters.models import Caster
        model = Caster
        fields = [
            'id', 'name', 'bio_link', 'stream_link'
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
    circuit_display = serializers.CharField()
    group = MatchGroupSerializer(read_only=True)

    primary_caster = MatchCasterSummarySerializer()
    secondary_casters = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name')
    
    class Meta:
        model = Match
        fields = [
            'id', 'home', 'away', 'circuit', 'circuit_display', 'round', 'group', 'start_time',
            'time_until', 'scheduled', 'primary_caster', 'secondary_casters',
            'result', 'vod_link'
        ]


class MatchUpdateSerializer(serializers.ModelSerializer):
    
    primary_caster = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False,
        queryset=Caster.objects.all(),
        style={'base_template': 'input.html'},
        required=False,
        allow_null=True
    )
        
    class Meta:
        model = Match
        fields = [
            'primary_caster', 'start_time'            
        ]

class CreateMatchSerializer(serializers.ModelSerializer):
    
    circuit = serializers.IntegerField(source='circuit_id', style={'base_template': 'input.html', 'placeholder': 'Circuit ID'})
    home = serializers.IntegerField(source='home_id', style={'base_template': 'input.html', 'placeholder': 'Home Team ID'})
    away = serializers.IntegerField(source='away_id', style={'base_template': 'input.html', 'placeholder': 'Away Team ID'})
    round = serializers.IntegerField(source='round_id', style={'base_template': 'input.html', 'placeholder': 'Round ID'})

    class Meta:
        model = Match
        fields = [
            'id', 'circuit', 'home', 'away', 'round'
        ]


    def validate(self, data):
        """Only users in 'service' account group can create matches."""
        user = self.context['request'].user

        has_permission, error = can_create_match(user, return_error_msg=True)

        if not has_permission:
            raise serializers.ValidationError(error)

        return data

