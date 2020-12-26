from rest_framework import serializers
from .leagues import CircuitSummarySerializer
from teams.models import Team


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = [
            'name', 'circuit', 'captain', 'members', 'modified', 'created'
        ]

class TeamSummarySerializer(serializers.HyperlinkedModelSerializer):
    
    detail_url = serializers.HyperlinkedIdentityField(view_name='team-detail')
    circuit = CircuitSummarySerializer()
    
    class Meta:
        model = Team
        fields = ['name', 'detail_url', 'circuit']
