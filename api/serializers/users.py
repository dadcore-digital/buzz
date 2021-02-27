from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        depth = 2
        fields = ['first_name']


class MeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        depth = 2
        fields = ['first_name']
