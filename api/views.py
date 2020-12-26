from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters
from django.contrib.auth.models import User
from .filters import EventFilter, PlayerFilter
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

class LeagueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = League.objects.all().order_by('name')
    serializer_class = LeagueSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SeasonViewSet(viewsets.ReadOnlyModelViewSet):
    
    def get_queryset(self):
        return Season.objects.filter(
            league=self.kwargs['league_pk']).order_by('name')

    serializer_class = SeasonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CircuitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Circuit.objects.all().order_by('name')
    serializer_class = CircuitSerializer


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

