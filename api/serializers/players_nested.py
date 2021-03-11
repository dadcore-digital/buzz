from rest_framework import serializers
from players.models import Player

class PlayerSerializerSummary(serializers.ModelSerializer):
    
    class Meta:
        model = Player
        fields = [
            'id', 'name', 'name_phonetic', 'pronouns', 'discord_username',
            'twitch_username', 'bio', 'emoji', 'avatar_url', 'modified',
            'created', 'award_summary'
        ]


