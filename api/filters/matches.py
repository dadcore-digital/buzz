from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
import pytz
from django_filters import rest_framework as filters
from matches.models import Match


class MatchFilter(filters.FilterSet):
    
    minutes = filters.NumberFilter(
        field_name='start_time', method='get_next_n_minutes',
        label='Get next n minutes'
    )

    hours = filters.NumberFilter(
        field_name='start_time', method='get_next_n_hours',
        label='Get next n hours'
    )
    days = filters.NumberFilter(
        field_name='start_time', method='get_next_n_days',
        label='Get next n days'
    )

    minutes = filters.NumberFilter(
        field_name='start_time', method='get_next_n_hours',
        label='Get next n minutes'
    )

    starts_in_minutes = filters.NumberFilter(
        field_name='start_time', method='get_starts_in_minutes',
        label='Starting in exact number of minutes'
    )

    home = filters.CharFilter(
        field_name='home__name', lookup_expr='icontains', label='Home Team Name'
    )

    away = filters.CharFilter(
        field_name='away__name', lookup_expr='icontains', label='Away Team Name'
    )

    team = filters.CharFilter(
        field_name='away__name', method='get_by_team_name',
        label='Home OR Away Team Name'
    )

    team_id = filters.CharFilter(
        field_name='away__id', method='get_by_team_id',
        label='Home OR Away Team ID'
    )

    teams = filters.CharFilter(
        field_name='away__name', method='get_by_team_names',
        label='Home AND Away Team Name'
    )

    winner = filters.CharFilter(
        field_name='result__winner__name', lookup_expr='icontains',
        label='Winning Team\'s Name'
    )

    loser = filters.CharFilter(
        field_name='result__loser__name', lookup_expr='icontains',
        label='Losing Team\'s Name'
    )

    dynasty = filters.CharFilter(
        field_name='away__dynasty__name', method='get_by_dynasty_name',
        label='Home OR Away Dynasty Name'
    )

    dynasties = filters.CharFilter(
        field_name='away__dynasty__name', method='get_by_dynasty_names',
        label='Home AND Away Dynasty Name'
    )

    scheduled = filters.BooleanFilter(
        field_name="start_time",
        lookup_expr='isnull',
        exclude=True,
        label='Has Been Scheduled',)

    status = filters.CharFilter(
        field_name='result__status', lookup_expr='icontains',
        label='Match Status (C, SF, DF)'
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

    circuit = filters.CharFilter(
        field_name='circuit__id',
        lookup_expr='exact',
        label='Circuit ID Number'
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

    round = filters.CharFilter(
        field_name='round__round_number',
        lookup_expr='exact',
        label='Round/Week Number'
    )

    primary_caster = filters.CharFilter(
        field_name='primary_caster__player__name',
        lookup_expr='icontains',
        label='Primary Caster Name'
    )

    now = pytz.utc.localize(datetime.utcnow())

    def get_next_n_minutes(self, queryset, field_name, value):
        time_threshold = timezone.now() + timedelta(minutes=int(value))

        return queryset.filter(
            start_time__gte=datetime.now(),
            start_time__lte=time_threshold
        )

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

    def get_starts_in_minutes(self, queryset, field_name, value):
        # Add a bit of wiggle room/bufer to start time in seconds
        current_minute = timezone.now().replace(second=0).replace(microsecond=0)
        time_floor = current_minute + timedelta(minutes=int(value)) 
        time_ceiling = time_floor + timedelta(seconds=59)

        return queryset.filter(
            start_time__gte=time_floor,
            start_time__lte=time_ceiling
        )

    def get_by_team_id(self, queryset, field_name, value):
    
        return queryset.filter(
            Q(home__id=value) |
            Q(away__id=value)
        )

    def get_by_team_name(self, queryset, field_name, value):

        return queryset.filter(
            Q(home__name__icontains=value) |
            Q(away__name__icontains=value)
        )

    def get_by_dynasty_name(self, queryset, field_name, value):

        return queryset.filter(
            Q(home__dynasty__name__icontains=value) |
            Q(away__dynasty__name__icontains=value)
        )

    def get_by_team_names(self, queryset, field_name, value):
        """
        Return match queryset for two team names.

        Takes two names separated by comma. Return queryset for case where
        either team name can be home or away.
        """
        teams_in_quotes = value.split('"')[1::2]        
        for team in teams_in_quotes:
            if ',' in team: 
                escaped_team = team.replace(',', '%2C').replace('"', '')
                value = value.replace(f'"{team}"', escaped_team)

        try:
            team_a, team_b = value.split(',')
        
        # Return all matches for just single team if only one valid team passed
        except ValueError:
            return queryset.filter(
                Q(home__name__icontains=value) |
                Q(away__name__icontains=value) 
        )

        # Remove extra whitespace, restore stripped values
        team_a = team_a.strip().replace('%2C', ',')
        team_b = team_b.strip().replace('%2C', ',')

        return queryset.filter(
            Q(home__name__icontains=team_a, away__name__icontains=team_b) |
            Q(home__name__icontains=team_b, away__name__icontains=team_a) 
        ).distinct()

    def get_by_dynasty_names(self, queryset, field_name, value):
        """
        Return match queryset for two team's dynasty names.

        Takes two dynasty names separated by comma. Return queryset for case where
        either team's dynasty name can be home or away.
        """
        dynasty_in_quotes = value.split('"')[1::2]        
        for dynasty in dynasty_in_quotes:
            if ',' in dynasty: 
                escaped_dynasty = dynasty.replace(',', '%2C').replace('"', '')
                value = value.replace(f'"{dynasty}"', escaped_dynasty)

        try:
            dynasty_a, dynasty_b = value.split(',')
        
        # Return all matches for just single team if only one valid team passed
        except ValueError:
            return queryset.filter(
                Q(home__dynasty__name__icontains=value) |
                Q(away__dynasty__name__icontains=value) 
        )

        # Remove extra whitespace, restore stripped values
        dynasty_a = dynasty_a.strip().replace('%2C', ',')
        dynasty_b = dynasty_b.strip().replace('%2C', ',')

        return queryset.filter(
            Q(home__dynasty__name__icontains=dynasty_a, away__dynasty__name__icontains=dynasty_b) |
            Q(home__dynasty__name__icontains=dynasty_b, away__dynasty__name__icontains=dynasty_a) 
        ).distinct()

    class Meta:
        model = Match
        fields = [
            'round', 'minutes', 'hours', 'days', 'starts_in_minutes', 'home',
            'away', 'team', 'team_id', 'teams', 'winner', 'loser',  'scheduled',
            'status', 'league', 'season', 'circuit', 'region', 'tier'
        ]