from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from leagues.models import League, Season, Circuit, Round, Bracket


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
            'league_pk': 'season__league__pk', 'season_pk': 'season__pk'
        }
    )

    rounds = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='rounds-detail',
        parent_lookup_kwargs={
            'league_pk': 'season__league__pk', 'season_pk': 'season__pk'
        }
    )

    brackets = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='brackets-detail',
        parent_lookup_kwargs={
            'league_pk': 'season__league__pk', 'season_pk': 'season__pk'
        }
    )

    class Meta:
        model = Season
        fields = [
            'name', 'regular_start', 'regular_end',
            'tournament_start', 'tournament_end', 'circuits', 'rounds',
            'brackets'
        ]

class SeasonSummarySerializer(serializers.ModelSerializer):
    league = LeagueSummarySerializer()
    

    class Meta:
        model = Season
        fields = ['id', 'name', 'league']

class CircuitSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Circuit
        depth = 2
        fields = [
            'region', 'tier', 'name', 'teams', 'verbose_name'
        ]

class CircuitSummarySerializer(serializers.ModelSerializer):
    
    season = SeasonSummarySerializer()

    class Meta:
        model = Circuit
        fields = ['season', 'region', 'tier', 'name', 'verbose_name']
    
        

class RoundSerializer(serializers.ModelSerializer):
    
    matches = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='match-detail'
    )

    class Meta:
        model = Round
        fields = ['round_number', 'name', 'matches']
    
    


class BracketSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bracket
        fields = ['name']

class RoundSummarySerializer(serializers.ModelSerializer):

    _href = serializers.HyperlinkedIdentityField(
        view_name='round-detail')

    class Meta:
        model = Round
        fields = ['round_number', '_href']
        
