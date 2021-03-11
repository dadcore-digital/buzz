from django_filters import rest_framework as filters
from players.models import Player

class PlayerFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains', label='Player Name')
    discord_username = filters.CharFilter(
        lookup_expr='icontains', label='Discord Username')
    twitch_username = filters.CharFilter(
        lookup_expr='icontains', label='Twitch Username')
    
    team = filters.CharFilter(
        field_name='teams__name', lookup_expr='icontains', label='Team Name')
    
    league = filters.CharFilter(
        field_name='teams__circuit__season__league__name',
        lookup_expr='icontains',
        label='League Name'
    )

    season = filters.CharFilter(
        field_name='teams__circuit__season__name',
        lookup_expr='icontains',
        label='Season Name'
    )

    region = filters.CharFilter(
        field_name='teams__circuit__region',
        lookup_expr='icontains',
        label='Team\'s Circuit Region Abbreviation'
    )

    tier = filters.CharFilter(
        field_name='teams__circuit__tier',
        lookup_expr='exact',
        label='Team\'s Circuit Tier Number'
    )

    award = filters.CharFilter(
        field_name='awards__award_category__name', lookup_expr='icontains',
        label='Award Name')


    class Meta:
        model = Player
        fields = [
            'name', 'discord_username', 'twitch_username', 'team', 'league',
            'season', 'region', 'tier', 'award'
        ]
