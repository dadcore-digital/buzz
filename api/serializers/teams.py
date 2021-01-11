from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from .leagues import CircuitSummarySerializer
from teams.models import Dynasty, Team

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
            'name', 'circuit', 'dynasty', 'captain', 'members', 'modified',
            'created', 'wins', 'losses'
        ]
        depth = 2

class TeamSummarySerializer(serializers.HyperlinkedModelSerializer):
    
    _href = serializers.HyperlinkedIdentityField(view_name='team-detail')

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
        fields = ['name', '_href', 'circuit', 'is_active', 'circuit_abbrev']

class TeamSummaryNoCircuitSerializer(serializers.HyperlinkedModelSerializer):
    
    _href = serializers.HyperlinkedIdentityField(view_name='team-detail')
    members = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name')

    class Meta:
        model = Team
        fields = ['name', '_href', 'wins', 'losses', 'members']


class DynastySerializer(serializers.ModelSerializer):
    
    teams = TeamSummarySerializer(many=True)

    class Meta:
        model = Dynasty
        fields = [
            'name', 'teams'
        ]
