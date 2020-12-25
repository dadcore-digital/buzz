from rest_framework import serializers
from django.contrib.auth.models import User, Group
from events.models import Event, EventLink
from leagues.models import League, Season, Circuit
from matches.models import Match
from players.models import Player
from streams.models import Stream
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

class MatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Match
        fields = [
            'home', 'away', 'circuit', 'start_time', 'primary_caster'
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

class PlayerSerializerNoDates(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = ['name', 'discord_username', 'twitch_username']


class EventLinkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EventLink
        fields = ['name', 'url']


class EventSerializer(serializers.ModelSerializer):
    links = EventLinkSerializer(many=True)
    organizers = PlayerSerializerNoDates(many=True)
    
    class Meta:
        model = Event
        fields = [
            'name', 'start_time', 'duration', 'description', 'organizers',
            'links', 'created', 'modified'
        ]

class StreamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stream
        fields = [
            'name', 'username', 'user_id', 'stream_id', 'service', 'is_live',
            'start_time', 'end_time'
        ]
