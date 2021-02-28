from django.contrib.auth.models import User
from rest_framework import serializers
from .players import PlayerSerializer

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        depth = 2
        fields = ['first_name']


class MeSerializer(serializers.ModelSerializer):

    player = PlayerSerializer()
            
    class Meta:
        model = User
        depth = 2
        fields = [
            'id', 'is_active', 'first_name', 'date_joined', 'last_login',
            'player'
        ]
