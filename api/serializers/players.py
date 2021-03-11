from rest_framework import serializers
from players.models import Player

class PlayerTeamSerializer(serializers.ModelSerializer):
    
    class Meta:
        from teams.models import Team
        model = Team

        fields = [
            'id', 'name', 'circuit', 'is_active', 'circuit_abbrev',
            'wins', 'losses'
        ]

class PlayerSerializer(serializers.ModelSerializer):
    
    teams = PlayerTeamSerializer(many=True)

    class Meta:
        model = Player
        depth = 1
        fields = [
            'id', 'name', 'name_phonetic', 'pronouns', 'discord_username',
            'twitch_username', 'bio', 'emoji', 'avatar_url', 'modified',
            'created', 'teams', 'award_summary', 'aliases'
        ]

        read_only_fields = [
            'id', 'discord_username', 'avatar_url', 'modified', 'created',
            'aliases'
        ]
