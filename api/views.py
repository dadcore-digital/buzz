from allauth.socialaccount.providers.discord.views import DiscordOAuth2Adapter
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404
from .filters import (
    AwardFilter, DynastyFilter, EventFilter, LeagueFilter, MatchFilter, PlayerFilter,
    TeamFilter, StreamFilter)
from .serializers.awards import AwardSerializer
from .serializers.casters import CasterSerializer
from .serializers.leagues import (
    LeagueSerializer, SeasonSerializer, CircuitSerializer, RoundSerializer,
    BracketSerializer)
from .permissions import CanAccessPlayer
from .serializers.beegame import PlayingSerializer, ReleaseSerializer
from .serializers.matches import MatchSerializer
from .serializers.teams import DynastySerializer, TeamSerializer
from .serializers.players import PlayerSerializer
from .serializers.events import EventSerializer
from .serializers.streams import StreamSerializer
from .serializers.users import MeSerializer, UserSerializer
from awards.models import Award
from beegame.models import Playing, Release
from events.models import Event
from leagues.models import League, Season, Circuit, Round, Bracket
from matches.models import Match
from casters.models import Caster
from players.models import Player
from streams.models import Stream
from teams.models import Dynasty, Team


class AwardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Award.objects.all().order_by('round__round_number')
    serializer_class = AwardSerializer
    filterset_class = AwardFilter

class LeagueViewSet(viewsets.ViewSet):
    serializer_class = LeagueSerializer

    def list(self, request):
        queryset = League.objects.filter()
        serializer = LeagueSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = League.objects.filter()

        league = get_object_or_404(queryset, pk=pk)
        serializer = LeagueSerializer(league, context={'request': request})
        return Response(serializer.data)


class SeasonViewSet(viewsets.ViewSet):
    
    serializer_class = SeasonSerializer

    def list(self, request, league_pk=None):
        queryset = Season.objects.filter(league=league_pk)
        serializer = SeasonSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None, league_pk=None):
        queryset = Season.objects.filter(pk=pk, league=league_pk)
        season = get_object_or_404(queryset, pk=pk)
        serializer = SeasonSerializer(season, context={'request': request})
        return Response(serializer.data)


class CircuitViewSet(viewsets.ViewSet):
    
    serializer_class = CircuitSerializer

    def list(self, request, league_pk=None, season_pk=None):
        queryset = Circuit.objects.filter(league=league_pk, season=season_pk)
        serializer = CircuitSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None, league_pk=None, season_pk=None):
        queryset = Circuit.objects.filter(pk=pk, season=season_pk)
        circuit = get_object_or_404(queryset, pk=pk)
        serializer = CircuitSerializer(circuit, context={'request': request})
        return Response(serializer.data)


class RoundViewSet(viewsets.ViewSet):
    
    serializer_class = RoundSerializer

    def list(self, request, league_pk=None, season_pk=None):
        queryset = Round.objects.filter(league=league_pk, season=season_pk)
        serializer = RoundSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None, league_pk=None, season_pk=None):
        queryset = Round.objects.filter(pk=pk, season=season_pk)
        round = get_object_or_404(queryset, pk=pk)
        serializer = RoundSerializer(round, context={'request': request})
        return Response(serializer.data)


class BracketViewSet(viewsets.ViewSet):
    
    serializer_class = BracketSerializer

    def list(self, request, league_pk=None, season_pk=None):
        queryset = Bracket.objects.filter(league=league_pk, season=season_pk)
        serializer = BracketSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None, league_pk=None, season_pk=None):
        queryset = Bracket.objects.filter(pk=pk, season=season_pk)
        bracket = get_object_or_404(queryset, pk=pk)
        serializer = BracketSerializer(bracket, context={'request': request})
        return Response(serializer.data)

class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Match.objects.all().order_by('round__round_number', 'start_time')
    serializer_class = MatchSerializer
    filterset_class = MatchFilter

class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.annotate(
        wins=Count('won_match_results', distinct=True),
        losses=Count('lost_match_results', distinct=True),
        
    )
    serializer_class = TeamSerializer
    filterset_class = TeamFilter

class DynastyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Dynasty.objects.all().order_by('name').distinct()
    serializer_class = DynastySerializer
    filterset_class = DynastyFilter

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all().order_by('name')
    permission_classes = [CanAccessPlayer]
    serializer_class = PlayerSerializer
    filterset_class = PlayerFilter

class CasterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Caster.objects.all().order_by('player__name')
    serializer_class = CasterSerializer

class StreamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stream.objects.all().order_by('-start_time')
    serializer_class = StreamSerializer
    filterset_class = StreamFilter

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = EventFilter

class PlayingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Playing.objects.all().order_by('-updated')
    serializer_class = PlayingSerializer

class ReleaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Release.objects.all().order_by('-released_on')
    serializer_class = ReleaseSerializer


class MeViewSet(viewsets.ViewSet):
    
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        
        serializer = MeSerializer(request.user, context={'request': request})
        return Response(serializer.data)
