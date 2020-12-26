from rest_framework import serializers
from awards.models import Award, AwardCategory

class AwardCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AwardCategory
        fields = ['name']


class AwardSerializer(serializers.ModelSerializer):

    award_category = AwardCategorySerializer()

    class Meta:
        model = Award
        fields = [
            'award_category', 'circuit', 'round', 'player', 'stats'
        ]
        depth = 2
