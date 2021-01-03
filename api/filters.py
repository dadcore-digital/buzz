from django.utils import timezone
from datetime import datetime, timedelta
import pytz
from django_filters import rest_framework as filters
from awards.models import Award
from events.models import Event
from leagues.models import League
from matches.models import Match
from players.models import Player
from streams.models import Stream
from teams.models import Team


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


    class Meta:
        model = Award
        fields = [
            'category_name', 'player_name', 'league', 'season', 'round',
            'region', 'tier'
        ]

class EventFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    organizer = filters.CharFilter(
        field_name='organizers__name', lookup_expr='icontains')

    minutes = filters.NumberFilter(
        field_name='start_time', method='get_next_n_minutes',
        label='Get next n hours'
    )

    hours = filters.NumberFilter(
        field_name='start_time', method='get_next_n_hours',
        label='Get next n hours'
    )
    days = filters.NumberFilter(
        field_name='start_time', method='get_next_n_days',
        label='Get next n days'
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
    class Meta:
        model = Event
        fields = ['name', 'minutes', 'hours', 'days', 'organizer']


class LeagueFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains', label='League Name')

    class Meta:
        model = League
        fields = ['name',]



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
        label='Get next n hours'
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

    winner = filters.CharFilter(
        field_name='result__winner__name', lookup_expr='icontains',
        label='Winning Team\'s Name'
    )

    loser = filters.CharFilter(
        field_name='result__loser__name', lookup_expr='icontains',
        label='Losing Team\'s Name'
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
        time_floor = timezone.now() + timedelta(minutes=int(value)) - timedelta(seconds=10)
        time_ceiling = timezone.now() + timedelta(days=int(value)) + timedelta(seconds=10)

        return queryset.filter(
            start_time__gte=time_floor,
            start_time__lte=time_ceiling
        )

    class Meta:
        model = Match
        fields = [
            'round', 'minutes', 'hours', 'days', 'starts_in_minutes', 'home',
            'away', 'winner', 'loser',  'scheduled', 'status', 'league',
            'season', 'region', 'tier' 
        ]


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

    dynasty = filters.CharFilter(
        field_name='dynasty__name',
        lookup_expr='icontains',
        label='Dynasty Name'
    )

    member = filters.CharFilter(
        field_name='members__name',
        lookup_expr='exact',
        label='Team Member Name'
    )


    class Meta:
        model = Team
        fields = [
            'name', 'league', 'season', 'region', 'tier', 'dynasty', 'member'
        ]


class StreamFilter(filters.FilterSet):
    username = filters.CharFilter(lookup_expr='icontains')
    is_live = filters.BooleanFilter()

    class Meta:
        model = Stream
        fields = ['is_live', 'username']
