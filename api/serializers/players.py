from rest_framework import serializers
from players.models import Player

class PlayerTeamSerializer(serializers.ModelSerializer):

    wins = serializers.IntegerField(read_only=True)
    losses = serializers.IntegerField(read_only=True)
    is_active = serializers.BooleanField(
        read_only=True, source='circuit.season.is_active')
    circuit_abbrev = serializers.SerializerMethodField()


    class Meta:
        from teams.models import Team
        model = Team

        fields = [
            'id', 'name', 'abbreviation', 'emoji', 'circuit', 'is_active',
            'wins', 'losses', 'circuit_abbrev'
        ]

    def get_circuit_abbrev(self, obj):
        return f'{obj.circuit.tier}{obj.circuit.region}'
        
class PlayerAwardCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        from awards.models import AwardCategory
        model = AwardCategory
        fields = ['id', 'name', 'discord_emoji']

class PlayerAwardGroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        from leagues.models import Group
        model = Group
        fields = ['id', 'name', 'number']


class PlayerAwardSerializer(serializers.ModelSerializer):
    
    award_category = PlayerAwardCategorySerializer(many=False, read_only=True)
    circuit = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    group = PlayerAwardGroupSerializer(read_only=True)

    class Meta:
        from awards.models import Award
        model = Award
        fields = [
            'id', 'award_category', 'circuit', 'group', 'round', 'stats'
        ]
        depth = 1

class PlayerSerializer(serializers.ModelSerializer):
    
    teams = PlayerTeamSerializer(many=True, read_only=True)
    awards = PlayerAwardSerializer(many=True, read_only=True)
    
    class Meta:
        model = Player
        depth = 1
        fields = [
            'id', 'name', 'name_phonetic', 'pronouns', 'discord_username',
            'twitch_username', 'bio', 'emoji', 'avatar_url', 'modified',
            'created', 'teams', 'awards', 'aliases'
        ]

        read_only_fields = [
            'id', 'discord_username', 'avatar_url', 'modified', 'created',
            'aliases'
        ]
