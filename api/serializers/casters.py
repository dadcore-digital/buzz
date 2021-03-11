from rest_framework import serializers
from casters.models import Caster
from .players_nested import PlayerSerializerSummary

class CasterSerializer(serializers.ModelSerializer):
    
    player = PlayerSerializerSummary()

    class Meta:
        model = Caster
        fields = [
            'name', 'player', 'bio_link', 'is_active', 'does_solo_casts',
            'stream_link'
        ]
