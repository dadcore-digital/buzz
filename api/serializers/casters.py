from rest_framework import serializers
from casters.models import Caster
from .players_nested import PlayerSerializerSummary

class CasterPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        from players.models import Player
        model = Player
        fields = [
            'id', 'name', 'name_phonetic', 'pronouns', 'discord_username',
            'twitch_username', 'bio', 'emoji', 'avatar_url', 'modified',
            'created'
        ]

class CasterSerializer(serializers.ModelSerializer):
    
    player = CasterPlayerSerializer()

    class Meta:
        model = Caster
        fields = [
            'id', 'name', 'player', 'bio_link', 'is_active', 'does_solo_casts',
            'stream_link'
        ]
