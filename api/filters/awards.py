from django_filters import rest_framework as filters
from awards.models import Award

class AwardFilter(filters.FilterSet):
    category_name = filters.CharFilter(
        field_name='award_category__name', lookup_expr='icontains',
        label='Award Category Name'
    )

    player_name = filters.CharFilter(
        field_name='player__name', lookup_expr='icontains',
        label='Player Name'
    )

    league = filters.CharFilter(
        field_name='circuit__season__league__name',
        lookup_expr='icontains',
        label='League Name'
    )

    season = filters.CharFilter(
        field_name='circuit__season__name',
        lookup_expr='icontains',
        label='Season Name'
    )

    round = filters.CharFilter(
        field_name='round__round_number',
        lookup_expr='exact',
        label='Round Number'
    )

    region = filters.CharFilter(
        field_name='circuit__region',
        lookup_expr='icontains',
        label='Circuit Region Abbreviation'
    )

    tier = filters.CharFilter(
        field_name='circuit__tier',
        lookup_expr='exact',
        label='Circuit Tier Number'
    )

    group = filters.CharFilter(
        field_name='group__id',
        lookup_expr='exact',
        label='Group ID Number'
    )

    class Meta:
        model = Award
        fields = [
            'category_name', 'player_name', 'league', 'season', 'round',
            'region', 'tier', 'group'
        ]
