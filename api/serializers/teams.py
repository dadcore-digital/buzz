from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from .leagues import CircuitSummarySerializer
from teams.models import Team


class TeamSerializer(serializers.ModelSerializer):

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
            'name', 'circuit', 'captain', 'members', 'modified', 'created'
        ]
        depth = 2

class TeamSummarySerializer(serializers.HyperlinkedModelSerializer):
    
    _href = serializers.HyperlinkedIdentityField(view_name='team-detail')

    # circuit = CircuitSummarySerializer(many=False, read_only=True)

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
        fields = ['name', '_href', 'circuit']
