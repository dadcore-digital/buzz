from rest_framework import serializers
from awards.models import Award, AwardCategory

class AwardCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AwardCategory
        fields = ['name']

class AwardCircuitSeasonSerializer(serializers.ModelSerializer):
    
    class Meta:
        from leagues.models import Season
        model = Season
        fields = ['id', 'name', ]
        
class AwardCircuitSerializer(serializers.ModelSerializer):
    season = AwardCircuitSeasonSerializer(many=False, read_only=True)

    class Meta:
        from leagues.models import Circuit
        model = Circuit
        fields = ['id', 'season', 'region', 'tier', 'name', 'verbose_name']

class AwardSerializer(serializers.ModelSerializer):

    award_category = AwardCategorySerializer()
    circuit = AwardCircuitSerializer(many=False, read_only=True)

    class Meta:
        model = Award
        fields = [
            'award_category', 'circuit', 'round', 'player', 'stats'
        ]
        depth = 1
