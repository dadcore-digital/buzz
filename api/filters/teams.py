from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
import pytz
from django_filters import rest_framework as filters
from teams.models import Dynasty, Team

class DynastyFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    team = filters.CharFilter(
        field_name='teams__name',
        lookup_expr='icontains',
        label='Team Name'
    )
    class Meta:
        model = Dynasty
        fields = ['name', 'team']


class TeamFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains', label='Team Name')
    
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

    circuit = filters.CharFilter(
        field_name='circuit__id',
        lookup_expr='exact',
        label='Circuit ID Number'
    )

    dynasty = filters.CharFilter(
        field_name='dynasty__name',
        lookup_expr='icontains',
        label='Dynasty Name'
    )

    is_active = filters.BooleanFilter(
        field_name='circuit__season__is_active',
        label='Is Active?'        
    )

    member = filters.CharFilter(
        field_name='members__name',
        lookup_expr='exact',
        label='Team Member Name'
    )


    class Meta:
        model = Team
        fields = [
            'name', 'league', 'season', 'circuit', 'region', 'tier', 'dynasty',
            'is_active', 'member'
        ]

