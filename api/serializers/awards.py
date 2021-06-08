from rest_framework import serializers
from awards.models import Award, AwardCategory, Stat, StatCategory
from awards.permissions import can_create_award

class AwardCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AwardCategory
        fields = ['id', 'name', 'discord_emoji']

class AwardCircuitSeasonSerializer(serializers.ModelSerializer):
    
    class Meta:
        from leagues.models import Season
        model = Season
        fields = ['id', 'name', ]

class AwardGroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        from leagues.models import Group
        model = Group
        fields = ['id', 'name', 'number']

class AwardCircuitSerializer(serializers.ModelSerializer):
    season = AwardCircuitSeasonSerializer(many=False, read_only=True)

    class Meta:
        from leagues.models import Circuit
        model = Circuit
        fields = ['id', 'season', 'region', 'tier', 'name', 'verbose_name']

class AwardSerializer(serializers.ModelSerializer):

    award_category = AwardCategorySerializer()
    circuit = AwardCircuitSerializer(many=False, read_only=True)
    group = AwardGroupSerializer(read_only=True)

    class Meta:
        model = Award
        fields = [
            'award_category', 'circuit', 'group', 'round', 'player', 'stats'
        ]
        depth = 1

class CreateAwardStatSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Stat
        fields = ['stat_category', 'total'] 

class CreateAwardSerializer(serializers.ModelSerializer):
    
    award_category = serializers.IntegerField(source='award_category_id', style={'base_template': 'input.html', 'placeholder': 'Award Category ID'})
    circuit = serializers.IntegerField(source='circuit_id', style={'base_template': 'input.html', 'placeholder': 'Circuit ID'})
    round = serializers.IntegerField(source='round_id', style={'base_template': 'input.html', 'placeholder': 'Round ID'})
    player = serializers.IntegerField(source='player_id', style={'base_template': 'input.html', 'placeholder': 'Player ID'})
    stats = CreateAwardStatSerializer(many=True, read_only=False)

    def create(self, validated_data):
        stats_data = validated_data.pop('stats')
        award = Award.objects.create(**validated_data)                                
        
        for data in stats_data:
            stat = Stat.objects.create(**data)
            award.stats.add(stat)
        
        return award

    def validate(self, data):
        """Only users in 'service' account group can create awards."""
        user = self.context['request'].user

        has_permission, error = can_create_award(user, return_error_msg=True)

        if not has_permission:
            raise serializers.ValidationError(error)

        return data


    class Meta:
        model = Award
        fields = [
            'award_category', 'circuit', 'round', 'player', 'stats'
        ]
        depth = 1

class StatCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = StatCategory
        fields = ['id', 'name']

class StatSerializer(serializers.ModelSerializer):
    
    stat_category = StatCategorySerializer()

    class Meta:
        model = Stat
        fields = ['id', 'stat_category', 'total']
