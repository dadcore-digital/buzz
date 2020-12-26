from rest_framework import serializers
from .awards import AwardSummarySerializer
from .teams import TeamSummarySerializer
from players.models import Player


class PlayerSerializer(serializers.ModelSerializer):
    
    teams = TeamSummarySerializer(many=True)
    awards = AwardSummarySerializer(many=True)

    class Meta:
        model = Player
        depth = 2
        fields = [
            'name', 'discord_username', 'twitch_username', 'modified', 'created',
            'teams', 'awards'
        ]

class PlayerSerializerNoDates(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Player
        fields = ['name', 'discord_username', 'twitch_username']

