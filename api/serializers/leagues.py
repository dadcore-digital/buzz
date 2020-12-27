from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from leagues.models import League, Season, Circuit, Round


class LeagueSerializer(serializers.HyperlinkedModelSerializer):
    
    seasons = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='seasons-detail',
        parent_lookup_kwargs={'league_pk': 'league__pk'}
    )

    class Meta:
        model = League
        fields = [
            'id', 'name', 'modified', 'created', 'seasons'
        ]


class LeagueSummarySerializer(serializers.HyperlinkedModelSerializer):

    _href = serializers.HyperlinkedIdentityField(
        view_name='leagues-detail'
    )

    class Meta:
        model = League
        fields = [
            'name', '_href'
        ]

class SeasonSerializer(serializers.HyperlinkedModelSerializer):

    circuits = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='circuits-detail',
        parent_lookup_kwargs={
            'league_pk': 'league__pk', 'season_pk': 'season__pk'
        }
    )

    class Meta:
        model = Season
        fields = [
            'name', 'regular_start', 'regular_end',
            'tournament_start', 'tournament_end', 'circuits'
        ]

class SeasonSummarySerializer(serializers.ModelSerializer):
    league = LeagueSummarySerializer()
    

    class Meta:
        model = Season
        fields = ['id', 'name', 'league']

class CircuitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Circuit
        fields = [
            'region', 'tier', 'name'
        ]

class CircuitSummarySerializer(serializers.ModelSerializer):
    
    season = SeasonSummarySerializer()

    class Meta:
        model = Circuit
        fields = ['season', 'region', 'tier', 'name']
        

class RoundSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Round
        fields = ['season', 'round_number', 'name', 'bracket']
        
class RoundSummarySerializer(serializers.ModelSerializer):

    _href = serializers.HyperlinkedIdentityField(
        view_name='round-detail')

    class Meta:
        model = Round
        fields = ['round_number', '_href']
        
