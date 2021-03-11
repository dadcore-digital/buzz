from django_filters import rest_framework as filters
from leagues.models import League, Season, Circuit

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

    class Meta:
        model = Circuit
        fields = ['name', 'is_active']

