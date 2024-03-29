from django_filters import rest_framework as filters
from leagues.models import Group, League, Season, Circuit

class GroupFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains', label='Group Name')

    is_active = filters.BooleanFilter(
        field_name='circuit__season__is_active',
        label='Season Is Active?'
    )


    class Meta:
        model = Group
        fields = ['name', 'circuit', 'is_active']


class LeagueFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains', label='League Name')

    class Meta:
        model = League
        fields = ['name',]

class SeasonFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains', label='Circuit Name')
    is_active = filters.BooleanFilter(
        field_name='is_active', label='Is Active?')

    class Meta:
        model = Season
        fields = ['name', 'is_active']

class CircuitFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains', label='Circuit Name')
    is_active = filters.BooleanFilter(
        field_name='season__is_active', label='Is Active?')

    registration_open = filters.BooleanFilter(
        field_name='season__registration_open', label='Registration Open?')

    rosters_open = filters.BooleanFilter(
        field_name='season__rosters_open', label='Rosters Open?')

    class Meta:
        model = Circuit
        fields = ['name', 'is_active']


