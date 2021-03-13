from rest_framework import serializers
from leagues.models import Circuit
from teams.models import Dynasty, Team

from .players_nested import PlayerSerializerSummary
from teams.permissions import can_create_team


class TeamPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        from players.models import Player
        model = Player
        fields = [
            'id', 'name', 'name_phonetic', 'pronouns', 'discord_username',
            'twitch_username', 'bio', 'emoji', 'avatar_url', 'modified',
            'created'
        ]

######################
# Team List Endpoint #
######################
class TeamSummarySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'circuit', 'is_active', 'circuit_abbrev',
            'win_count', 'loss_count'
        ]

class DynastySerializer(serializers.ModelSerializer):
    
    teams = TeamSummarySerializer(many=True)

    class Meta:
        model = Dynasty
        fields = [
            'name', 'teams'
        ]

class DynastyNoTeamsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dynasty
        fields = ['name']

class TeamSerializer(serializers.ModelSerializer):

    members = TeamPlayerSerializer(many=True, read_only=True)
    captain = TeamPlayerSerializer(many=False, read_only=True)

    circuit = serializers.PrimaryKeyRelatedField(
        many=False, queryset=Circuit.objects.filter(season__is_active=True))

    wins = serializers.IntegerField(read_only=True)
    losses = serializers.IntegerField(read_only=True)

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'circuit', 'is_active', 'can_add_members', 'dynasty',
            'captain', 'members', 'modified', 'created', 'wins', 'losses' 
        ]
        depth = 2

        read_only_fields = [
            'id',  'is_active', 'can_add_members', 'dynasty',
            'captain', 'members', 'modified', 'created', 'wins', 'losses'
        ]
    
    def validate(self, data):
        user = self.context['request'].user
        has_permission = can_create_team(data.get('circuit'), user)
        
        if has_permission:
            return data

        raise serializers.ValidationError('Permission Denied')

########################
# Team Detail Endpoint #
########################
class TeamDetailMatchRoundSummarySerializer(serializers.ModelSerializer):
    
    number = serializers.DecimalField(
        source='round_number', max_digits=4, decimal_places=2)

    class Meta:
        from leagues.models import Round
        model = Round
        fields = ['number', 'name']


class TeamDetailMatchResultSerializer(serializers.ModelSerializer):
    
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
        from matches.models import Result
        model = Result
        fields = [
            'id', 'status', 'winner', 'loser', 'sets_home', 'sets_away',
            'sets_total'
        ]


class TeamDetailMatchTeamSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Team
        fields = [
            'id', 'name'
        ]

class TeamDetailMatchCasterSummarySerializer(serializers.ModelSerializer):
    
    class Meta:
        from casters.models import Caster
        model = Caster
        fields = [
            'name', 'bio_link', 'stream_link'
        ]

class TeamDetailMatchSerializer(serializers.ModelSerializer):
    
    home = TeamDetailMatchTeamSerializer()
    away = TeamDetailMatchTeamSerializer()

    round = TeamDetailMatchRoundSummarySerializer()
    result = TeamDetailMatchResultSerializer()

    primary_caster = TeamDetailMatchCasterSummarySerializer()
    secondary_casters = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name')
    
    class Meta:
        from matches.models import Match
        model = Match
        fields = [
            'id', 'home', 'away', 'round', 'start_time',
            'time_until', 'scheduled', 'primary_caster', 'secondary_casters',
            'result', 'vod_link'
        ]

class TeamDetailSerializer(serializers.ModelSerializer):
    
    members = TeamPlayerSerializer(many=True, read_only=True)
    captain = TeamPlayerSerializer(many=False, read_only=True)

    circuit = serializers.PrimaryKeyRelatedField(
        many=False, queryset=Circuit.objects.filter(season__is_active=True))

    home_matches = TeamDetailMatchSerializer(many=True, read_only=True)
    away_matches = TeamDetailMatchSerializer(many=True, read_only=True)

    wins = serializers.IntegerField(read_only=True)
    losses = serializers.IntegerField(read_only=True)

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'circuit', 'is_active', 'can_add_members', 'dynasty',
            'captain', 'home_matches', 'away_matches', 'members', 'modified',
            'created', 'wins', 'losses' 
        ]
        depth = 2

        read_only_fields = [
            'id',  'is_active', 'can_add_members', 'dynasty',
            'captain', 'home_matches', 'away_matches', 'members', 'modified',
            'created', 'wins', 'losses'
        ]
    
    def validate(self, data):
        user = self.context['request'].user
        has_permission = can_create_team(data.get('circuit'), user)
        
        if has_permission:
            return data

        raise serializers.ValidationError('Permission Denied')

