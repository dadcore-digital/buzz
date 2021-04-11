from django_filters import rest_framework as filters
from casters.models import Caster

class CasterFilter(filters.FilterSet):
    is_active = filters.BooleanFilter(
        field_name='is_active', label='Is Active?')
    does_solo_casts = filters.BooleanFilter(
        field_name='does_solo_casts', label='Does Solo Casts?')        

    class Meta:
        model = Caster
        fields = [
            'is_active', 'does_solo_casts'
        ]
