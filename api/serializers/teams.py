from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from leagues.models import Circuit
from teams.models import Dynasty, Team
from .players_nested import PlayerSerializerSummary
from teams.permissions import can_create_team

class TeamSummarySerializer(serializers.HyperlinkedModelSerializer):
    
    circuit = NestedHyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='circuits-detail',
        parent_lookup_kwargs={
            'league_pk': 'league__pk', 'season_pk': 'season__pk'
        }
    )

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'circuit', 'is_active', 'circuit_abbrev',
            'wins', 'losses'
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

    members = PlayerSerializerSummary(many=True, read_only=True)
    captain = PlayerSerializerSummary(many=False, read_only=True)

    circuit = serializers.PrimaryKeyRelatedField(
        many=False, queryset=Circuit.objects.filter(season__is_active=True))

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

class TeamSummaryNoCircuitSerializer(serializers.HyperlinkedModelSerializer):
    
    members = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name')
    dynasty = DynastyNoTeamsSerializer()

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'is_active', 'wins', 'losses', 'members',
            'dynasty', 'wins', 'losses'
        ]

class TeamSummaryNoCircuitMemberDetailSerializer(serializers.ModelSerializer):
    
    dynasty = DynastyNoTeamsSerializer()
    members = PlayerSerializerSummary(many=True)

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'is_active', 'wins', 'losses', 'members',
            'dynasty', 'wins', 'losses'
        ]

        depth = 2

class TeamSummaryBriefSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'is_active', 'wins', 'losses', 'wins',
            'losses', 'circuit_abbrev'
        ]


