from rest_framework import serializers
from django.contrib.auth.models import User, Group
from leagues.models import League, Season, Circuit
from players.models import Player
from teams.models import Team


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

class CircuitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Circuit
        fields = [
            'season', 'region', 'tier', 'name'
        ]

class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = [
            'name', 'circuit', 'captain', 'members', 'modified', 'created'
        ]

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = [
            'name', 'discord_username', 'twitch_username', 'modified', 'created'
        ]

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username']