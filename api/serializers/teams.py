from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from teams.models import Dynasty, Team


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

    wins = serializers.IntegerField()
    losses = serializers.IntegerField()

    circuit = NestedHyperlinkedRelatedField(
            many=False,
            read_only=True,
            view_name='circuits-detail',
            parent_lookup_kwargs={
                'league_pk': 'league__pk', 'season_pk': 'season__pk'
            },
        )

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'circuit', 'is_active', 'dynasty', 'captain',
            'members', 'modified', 'created', 'wins', 'losses'
        ]
        depth = 2

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
            'losses'
        ]


