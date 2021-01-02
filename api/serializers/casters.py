from rest_framework import serializers
from casters.models import Caster
from .players import PlayerSerializerNoDates

class CasterSerializer(serializers.ModelSerializer):
    
    player = PlayerSerializerNoDates()

    class Meta:
        model = Caster
        fields = [
            'player', 'bio_link', 'is_active', 'does_solo_casts', 'stream_link'
        ]


class CasterSummarySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Caster
        fields = [
            'bio_link', 'stream_link'
        ]
