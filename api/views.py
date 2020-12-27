from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .filters import EventFilter, PlayerFilter, TeamFilter
from .serializers.awards import AwardSerializer
from .serializers.leagues import (
    LeagueSerializer, SeasonSerializer, CircuitSerializer, RoundSerializer)
from .serializers.matches import MatchSerializer
from .serializers.teams import TeamSerializer
from .serializers.players import PlayerSerializer
from .serializers.events import EventSerializer
from .serializers.streams import StreamSerializer
from awards.models import Award
from events.models import Event
from leagues.models import League, Season, Circuit, Round
from matches.models import Match
from players.models import Player
from streams.models import Stream
from teams.models import Team


class AwardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer

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


class RoundViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Round.objects.all()
    serializer_class = RoundSerializer

class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Match.objects.all().order_by('start_time')
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all().order_by('name')
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = TeamFilter

class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Player.objects.all().order_by('name')
    serializer_class = PlayerSerializer
    filterset_class = PlayerFilter

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = EventFilter

class StreamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

