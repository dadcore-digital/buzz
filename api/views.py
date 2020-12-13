from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth.models import User
from .serializers import (
    LeagueSerializer, SeasonSerializer, CircuitSerializer, MatchSerializer,
    TeamSerializer, PlayerSerializer, UserSerializer) 
from leagues.models import League, Season, Circuit
from matches.models import Match
from players.models import Player
from teams.models import Team


class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all().order_by('name')
    serializer_class = LeagueSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all().order_by('name')
    serializer_class = SeasonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CircuitViewSet(viewsets.ModelViewSet):
    queryset = Circuit.objects.all().order_by('name')
    serializer_class = CircuitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all().order_by('start_time')
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().order_by('name')
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all().order_by('name')
    serializer_class = PlayerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
