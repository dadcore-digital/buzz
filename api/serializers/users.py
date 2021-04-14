from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        depth = 2
        fields = ['first_name']

class MePlayerTeamSerializer(serializers.ModelSerializer):
    
    wins = serializers.IntegerField(read_only=True)
    losses = serializers.IntegerField(read_only=True)
    is_active = serializers.BooleanField(
        read_only=True, source='circuit.season.is_active')
    circuit_abbrev = serializers.SerializerMethodField()
    circuit_display = serializers.SerializerMethodField()


    class Meta:
        from teams.models import Team
        model = Team

        fields = [
            'id', 'name', 'circuit', 'is_active', 'wins', 'losses',
            'circuit_abbrev', 'circuit_display' 
        ]

    def get_circuit_abbrev(self, obj):
        return f'{obj.circuit.tier}{obj.circuit.region}'

    def get_circuit_display(self, obj):
        league_name = obj.circuit.season.league.name
        if league_name.startswith('Indy'):
            league_name = 'IGL'
        elif league_name.startswith('Bee'):
            league_name = 'BGL'

        return f'{league_name} {obj.circuit.season.name} {obj.circuit.tier}{obj.circuit.region}'



class MePlayerAwardCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        from awards.models import AwardCategory
        model = AwardCategory
        fields = ['id', 'name']

class PlayerAwardSerializer(serializers.ModelSerializer):
    
    award_category = MePlayerAwardCategorySerializer(many=False, read_only=True)
    circuit = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        from awards.models import Award
        model = Award
        fields = [
            'id', 'award_category', 'circuit', 'round', 'stats'
        ]
        depth = 1

class MePlayerSerializer(serializers.ModelSerializer):
    
    teams = MePlayerTeamSerializer(many=True, read_only=True)
    awards = PlayerAwardSerializer(many=True, read_only=True)

    class Meta:
        from players.models import Player
        model = Player
        depth = 2
        fields = [
            'id', 'name', 'name_phonetic', 'pronouns', 'discord_username',
            'twitch_username', 'bio', 'emoji', 'avatar_url', 'modified',
            'created', 'teams', 'awards'
        ]

class MeSerializer(serializers.ModelSerializer):

    player = MePlayerSerializer()
            
    class Meta:
        model = User
        depth = 2
        fields = [
            'id', 'is_active', 'first_name', 'date_joined', 'last_login',
            'player'
        ]
