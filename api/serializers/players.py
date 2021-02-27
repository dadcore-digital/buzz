from rest_framework import serializers
from .awards import AwardSummarySerializer
from .teams import TeamSummaryNoCircuitMemberDetailSerializer
from players.models import Player


class PlayerSerializer(serializers.ModelSerializer):
    
    teams = TeamSummaryNoCircuitMemberDetailSerializer(many=True)

    class Meta:
        model = Player
        depth = 1
        fields = [
            'name', 'name_phonetic', 'pronouns', 'discord_username',
            'twitch_username', 'bio', 'modified', 'created', 'teams'
        ]

        # fields = [
        #     'name', 'name_phonetic', 'pronouns', 'discord_username',
        #     'twitch_username', 'bio', 'modified', 'created', 'teams', 'aliases',
        #     'award_summary'
        # ]

class PlayerSerializerNoDates(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Player
        fields = ['id', 'name', 'discord_username', 'twitch_username']

