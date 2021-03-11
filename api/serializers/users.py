from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        depth = 2
        fields = ['first_name']


class MePlayerSerializer(serializers.ModelSerializer):
    
    class Meta:
        from players.models import Player
        model = Player
        depth = 2
        fields = [
            'id', 'name', 'name_phonetic', 'pronouns', 'discord_username',
            'twitch_username', 'bio', 'emoji', 'avatar_url', 'modified',
            'created', 'teams', 'award_summary'
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
