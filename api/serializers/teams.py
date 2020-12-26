from rest_framework import serializers
from teams.models import Team


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = [
            'name', 'circuit', 'captain', 'members', 'modified', 'created'
        ]
