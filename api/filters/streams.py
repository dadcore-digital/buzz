from django.utils import timezone
from datetime import datetime, timedelta
from django_filters import rest_framework as filters
from streams.models import Stream, StreamerBlacklist

class StreamFilter(filters.FilterSet):
    username = filters.CharFilter(lookup_expr='icontains')
    is_live = filters.BooleanFilter()

    def get_started_n_minutes_ago(self, queryset, field_name, value):
        # Add a bit of wiggle room/bufer to start time in seconds
        current_minute = timezone.now().replace(second=0).replace(microsecond=0)
        time_floor = current_minute - timedelta(minutes=int(value)) 
        time_ceiling = time_floor + timedelta(seconds=59)

        return queryset.filter(start_time__gte=time_floor,start_time__lte=time_ceiling)

    def get_blessed_streams(self, queryset, field_name, value):
        
        if value == True:
            blacklisted_streamers = StreamerBlacklist.objects.all().values_list(
                'username', flat=True)

            return queryset.exclude(username__in=blacklisted_streamers)

        return queryset.all()


    started_n_minutes_ago = filters.NumberFilter(
        field_name='start_time', method='get_started_n_minutes_ago',
        label='Started in exactly n number of minutes ago'
    )

    blessed = filters.BooleanFilter(
        field_name='blessed', method='get_blessed_streams',
        label='Include only "blessed" streams'
    )

    class Meta:
        model = Stream
        fields = [
            'is_live', 'username', 'started_n_minutes_ago', 'blessed']
