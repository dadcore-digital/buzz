from rest_framework import serializers
from leagues.models import League, Season, Circuit, Round

class LeagueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = League
        fields = [
            'name', 'modified', 'created'
        ]


class LeagueSummarySerializer(serializers.HyperlinkedModelSerializer):

    detail_url = serializers.HyperlinkedIdentityField(
        view_name='league-detail'
    )

    class Meta:
        model = League
        fields = [
            'name', 'detail_url'
        ]

class SeasonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Season
        fields = [
            'name', 'league', 'regular_start', 'regular_end', 'playoffs_start',
            'playoffs_end'
        ]

class SeasonSummarySerializer(serializers.ModelSerializer):
    league = LeagueSummarySerializer()
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='season-detail'
    )

    class Meta:
        model = Season
        fields = ['name', 'league', 'detail_url']

class CircuitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Circuit
        fields = [
            'season', 'region', 'tier', 'name'
        ]

class CircuitSummarySerializer(serializers.ModelSerializer):
    
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='circuit-detail')
    season = SeasonSummarySerializer()

    class Meta:
        model = Circuit
        fields = [
            'season', 'region', 'tier', 'name', 'detail_url'
        ]
        

class RoundSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Round
        fields = ['season', 'round_number', 'name', 'bracket']
        
class RoundSummarySerializer(serializers.ModelSerializer):

    detail_url = serializers.HyperlinkedIdentityField(
        view_name='round-detail')

    class Meta:
        model = Round
        fields = ['round_number', 'detail_url']
        
