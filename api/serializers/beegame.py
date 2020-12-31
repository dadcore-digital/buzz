from rest_framework import serializers
from beegame.models import Playing, Release

class PlayingSerializer(serializers.ModelSerializer):
    
    platform = serializers.CharField(source='get_platform_display')

    class Meta:
        model = Playing
        fields = [
            'updated', 'total', 'platform', 'operating_system', 'ranked_total',
            'quickplay_total', 'custom_total'
        ]

class ReleaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Release
        fields = [
            'version', 'buildid', 'released_on', 'title', 'message', 'platform'
        ]
