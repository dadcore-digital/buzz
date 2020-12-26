from rest_framework import serializers
from leagues.models import League, Season, Circuit

class LeagueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = League
        fields = [
            'name', 'modified', 'created'
        ]

class SeasonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Season
        fields = [
            'name', 'league', 'regular_start', 'regular_end', 'playoffs_start',
            'playoffs_end'
        ]

class SeasonSerializerSummary(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Season
        fields = ['name']

class CircuitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Circuit
        fields = [
            'season', 'region', 'tier', 'name'
        ]
