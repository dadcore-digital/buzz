from rest_framework import serializers
from .teams import TeamSummaryNoCircuitMemberDetailSerializer
from players.models import Player



class PlayerSerializer(serializers.ModelSerializer):
    
    teams = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name')

    class Meta:
        model = Player
        depth = 1
        fields = [
            'name', 'name_phonetic', 'pronouns', 'discord_username',
            'twitch_username', 'bio', 'emoji', 'avatar_url', 'modified',
            'created', 'teams', 'award_summary'
        ]

class PlayerSerializerFullTeam(serializers.ModelSerializer):
    
    teams = TeamSummaryNoCircuitMemberDetailSerializer(many=True)

    class Meta:
        model = Player
        depth = 1
        fields = [
            'name', 'name_phonetic', 'pronouns', 'discord_username',
            'twitch_username', 'bio', 'emoji', 'avatar_url', 'modified',
            'created', 'teams', 'award_summary'
        ]


