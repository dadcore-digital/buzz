from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
import pytz
from django_filters import rest_framework as filters
from awards.models import Award
from events.models import Event
from leagues.models import League
from matches.models import Match
from players.models import Player
from streams.models import Stream, StreamerBlacklist
from teams.models import Dynasty, Team


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

class DynastyFilter(filter.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    team = filters.CharFilter(
        field_name='teams__name',
        lookup_expr='icontains',
        label='Team Name'
    )
    class Meta:
        model = Dynasty
        fields = ['name', 'team']


class EventFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    organizer = filters.CharFilter(
        field_name='organizers__name', lookup_expr='icontains')

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

    def get_by_team_name(self, queryset, field_name, value):

        return queryset.filter(
            Q(home__name__icontains=value) |
            Q(away__name__icontains=value)
        )

    def get_by_team_names(self, queryset, field_name, value):
        """
        Return match queryset for two team names.

        Takes two names separated by comma. Return queryset for case where
        either team name can be home or team.
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

    class Meta:
        model = Match
        fields = [
            'round', 'minutes', 'hours', 'days', 'starts_in_minutes', 'home',
            'away', 'team', 'teams', 'winner', 'loser',  'scheduled', 'status',
            'league', 'season', 'region', 'tier'
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
