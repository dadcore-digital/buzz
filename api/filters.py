from django.utils import timezone
from datetime import datetime, timedelta
import pytz
from django_filters import rest_framework as filters
from events.models import Event
now = pytz.utc.localize(datetime.utcnow())

class EventFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    organizer = filters.CharFilter(
        field_name='organizers__name', lookup_expr='icontains')
    hours = filters.NumberFilter(
        field_name='start_time', method='get_next_n_hours',
        label='Get next n hours'
    )
    days = filters.NumberFilter(
        field_name='start_time', method='get_next_n_days',
        label='Get next n days'
    )

    now = pytz.utc.localize(datetime.utcnow())

    def get_next_n_hours(self, queryset, field_name, value):
        time_threshold = timezone.now() + timedelta(hours=int(value))

        return queryset.filter(
            start_time__gte=datetime.now(),
            start_time__lte=time_threshold
        )

    def get_next_n_days(self, queryset, field_name, value):
        time_threshold = timezone.now() + timedelta(days=int(value))

        return queryset.filter(
            start_time__gte=datetime.now(),
            start_time__lte=time_threshold
        )

    class Meta:
        model = Event
        fields = ['name', 'hours', 'days', 'organizer']
