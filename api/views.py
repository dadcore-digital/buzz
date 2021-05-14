from allauth.socialaccount.providers.discord.views import DiscordOAuth2Adapter
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Count, OuterRef, Prefetch, Sum, Q, Subquery, Case, When, F, IntegerField
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect
from .filters.awards import AwardFilter
from .filters.casters import CasterFilter
from .filters.events import EventFilter    
from .filters.leagues import CircuitFilter, LeagueFilter, SeasonFilter
from .filters.matches import MatchFilter
from .filters.players import PlayerFilter
from .filters.streams import StreamFilter
from .filters.teams import DynastyFilter, TeamFilter
from .serializers.awards import AwardSerializer
from .serializers.casters import CasterSerializer
from .serializers.leagues import (
    LeagueSerializer, SeasonSerializer, CircuitSerializer, GroupSerializer,
    RoundSerializer)
from api import permissions
from .serializers.beegame import PlayingSerializer, ReleaseSerializer
from .serializers.matches import (
    GameSerializer, CreateMatchSerializer, MatchSerializer,
    MatchUpdateSerializer, ResultSerializer, ResultDetailSerializer,
    SetSerializer, SetDetailSerializer
)
from .serializers.teams import (
    DynastySerializer, JoinTeamSerializer, TeamSerializer, TeamDetailSerializer)
from .serializers.players import PlayerSerializer
from .serializers.events import EventSerializer
from .serializers.streams import StreamSerializer
from .serializers.users import MeSerializer, UserSerializer
from awards.models import Award
from beegame.models import Playing, Release
from events.models import Event
from leagues.models import League, Season, Circuit, Group, Round
from matches.models import Game, Match, Result, Set
from matches.permissions import can_update_match
from casters.models import Caster
from players.models import Player
from streams.models import Stream
from teams.models import Dynasty, Team
from teams.permissions import can_regenerate_team_invite_code


class AwardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Award.objects.all().order_by('round__round_number')
    serializer_class = AwardSerializer
    filterset_class = AwardFilter

class LeagueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = League.objects.all().order_by('name')
    filterset_class = LeagueFilter
    serializer_class = LeagueSerializer

class SeasonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Season.objects.all().order_by('name')
    filterset_class = SeasonFilter
    serializer_class = SeasonSerializer

class CircuitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Circuit.objects.select_related('season')
    queryset = queryset.prefetch_related(
        Prefetch('teams', queryset=Team.objects.annotate(
            wins=Count('won_match_results', distinct=True)).annotate(losses=Count('lost_match_results', distinct=True))),
        Prefetch('teams__members')            
    ).order_by('id')
    
    filterset_class = CircuitFilter
    serializer_class = CircuitSerializer

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.select_related('circuit')
    queryset = queryset.prefetch_related(
        Prefetch('teams', queryset=Team.objects.annotate(
            wins=Count('won_match_results', distinct=True)).annotate(losses=Count('lost_match_results', distinct=True))),
        Prefetch('teams__members')            
    ).order_by('id')
    
    serializer_class = GroupSerializer

class RoundViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Round.objects.all().order_by('name')
    serializer_class = RoundSerializer

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all().order_by('round__round_number', 'start_time')
    queryset = queryset.select_related('circuit')
    queryset = queryset.select_related('round')


    queryset = queryset.prefetch_related(
        Prefetch('home', Team.objects.annotate(
            wins=Count('won_match_results', distinct=True)).annotate(
                losses=Count('lost_match_results', distinct=True))
        ),
        Prefetch('home__members')
    )
    queryset = queryset.prefetch_related(
        Prefetch('away', Team.objects.annotate(
            wins=Count('won_match_results', distinct=True)).annotate(
                losses=Count('lost_match_results', distinct=True))
        ),
        Prefetch('away__members')
    )

    queryset = queryset.select_related('primary_caster__player')
    queryset = queryset.prefetch_related('secondary_casters__player')
    queryset = queryset.prefetch_related('circuit__season')

    queryset = queryset.prefetch_related(
        Prefetch('result', Result.objects.annotate(
            sets_total=Coalesce(Count('sets'), 0)
        ).annotate(sets_home=Count(
                Case(
                    When(
                        sets__winner=F('match__home'), then=1),
                        output_field=IntegerField(),
                    )
                )
        ).annotate(sets_away=Count(
                Case(
                    When(
                        sets__winner=F('match__away'), then=1),
                        output_field=IntegerField(),
                    )
                )
            )
        ),
        Prefetch('result__sets'),
        Prefetch('result__winner'),
        Prefetch('result__loser'),
    )
    
    
    serializer_class = MatchSerializer
    filterset_class = MatchFilter
    permission_classes = [
        permissions.CanReadMatch|permissions.CanUpdateMatch|permissions.CanCreateMatch
    ]
    http_method_names = ['get', 'patch', 'post']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateMatchSerializer

        return MatchSerializer 

    def create(self, request, *args, **kwargs):
        """
        Redirect to result detail view on creation.
        """
        response = super(MatchViewSet, self).create(request, *args, **kwargs)
        url = reverse('match-detail', kwargs={'pk': response.data['id']})
        return redirect(url)

    def partial_update(self, request, pk=None):
        match = Match.objects.filter(id=pk).first()

        partial_serializer = MatchUpdateSerializer(
            match, data=request.data, context={'request': request})
        
        if partial_serializer.is_valid():
            if can_update_match(match, request.user):
                match =partial_serializer.save()

                full_serializer = MatchSerializer(match)
                
                return Response(full_serializer.data) 

        raise PermissionDenied(
            'Permission Error: Either you are not a team captain associated with this match, or it has already occurred.')
    
class ResultViewSet(viewsets.ModelViewSet):

    queryset = Result.objects.all().order_by('id')
    queryset = queryset.prefetch_related('loser__circuit__season')
    queryset = queryset.prefetch_related('winner__circuit__season')
    queryset = queryset.prefetch_related('sets__winner__circuit__season')
    queryset = queryset.prefetch_related('sets__loser__circuit__season')
    
    serializer_class = ResultSerializer

    permission_classes = [
        permissions.CanReadResult|permissions.CanCreateResult
    ]

    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        """
        Redirect to result detail view on creation.
        """
        response = super(ResultViewSet, self).create(request, *args, **kwargs)
        url = reverse('results-detail', kwargs={'pk': response.data['id']})
        return redirect(url)

    def perform_create(self, serializer):
        player, created = Player.objects.get_or_create(user=self.request.user)
        result = serializer.save(created_by=player)
        
    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()       
        queryset = queryset.prefetch_related('loser__circuit__season')
        queryset = queryset.prefetch_related('winner__circuit__season')
        queryset = queryset.prefetch_related('sets__winner__circuit__season')
        queryset = queryset.prefetch_related('sets__loser__circuit__season')

        result = queryset.filter(id=pk).first()
        serializer = ResultDetailSerializer(result, context={'request': request})
        return Response(serializer.data)

class SetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Set.objects.all().order_by('id')
    queryset = queryset.prefetch_related('loser__circuit')
    queryset = queryset.prefetch_related('winner__circuit')

    serializer_class = SetSerializer

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()       
        queryset = queryset.prefetch_related('loser__circuit')
        queryset = queryset.prefetch_related('winner__circuit')

        set = queryset.filter(id=pk).first()
        serializer = SetDetailSerializer(set, context={'request': request})
        return Response(serializer.data)
        
class GameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Game.objects.all().order_by('id')
    serializer_class = GameSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().order_by('name')
    queryset = queryset.select_related('captain')
    queryset = queryset.select_related('circuit')
    queryset = queryset.select_related('dynasty')
    queryset = queryset.prefetch_related('members')
    queryset = queryset.select_related('circuit__season')
    queryset = queryset.annotate(wins=Count('won_match_results', distinct=True))
    queryset = queryset.annotate(losses=Count('lost_match_results', distinct=True))

    permission_classes = [permissions.CanUpdateTeam]

    serializer_class = TeamSerializer
    filterset_class = TeamFilter

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.prefetch_related('home_matches__primary_caster')
        queryset = queryset.prefetch_related('away_matches__primary_caster')
        queryset = queryset.prefetch_related('home_matches__secondary_casters')
        queryset = queryset.prefetch_related('away_matches__secondary_casters')
        queryset = queryset.prefetch_related('home_matches__round')
        queryset = queryset.prefetch_related('away_matches__round')

        queryset = queryset.prefetch_related(
            Prefetch('home_matches__result', Result.objects.annotate(
                sets_total=Coalesce(Count('sets'), 0)
            ).annotate(sets_home=Count(
                    Case(
                        When(
                            sets__winner=F('match__home'), then=1),
                            output_field=IntegerField(),
                        )
                    )
            ).annotate(sets_away=Count(
                    Case(
                        When(
                            sets__winner=F('match__away'), then=1),
                            output_field=IntegerField(),
                        )
                    )
                )
            ),
            Prefetch('home_matches__result__match__home__members'),
            Prefetch('home_matches__result__match__away__members'),
        )
 
        queryset = queryset.prefetch_related(
            Prefetch('away_matches__result', Result.objects.annotate(
                sets_total=Coalesce(Count('sets'), 0)
            ).annotate(sets_home=Count(
                    Case(
                        When(
                            sets__winner=F('match__home'), then=1),
                            output_field=IntegerField(),
                        )
                    )
            ).annotate(sets_away=Count(
                    Case(
                        When(
                            sets__winner=F('match__away'), then=1),
                            output_field=IntegerField(),
                        )
                    )
                )
            ),
            Prefetch('away_matches__result__match__home__members'),
            Prefetch('away_matches__result__match__away__members'),
        )            

        team = queryset.filter(id=pk).first()
        serializer = TeamDetailSerializer(team, context={'request': request})
        return Response(serializer.data)

    def perform_create(self, serializer):
        player, created = Player.objects.get_or_create(user=self.request.user)
        team = serializer.save(captain=player)
        team.members.add(player)
    
    @action(
        methods=['post'], detail=True,
        permission_classes=[permissions.CanReadTeam]
    )
    def join(self, request, pk=None):
        team = Team.objects.filter(pk=pk).first()
        user = request.user
        context = {'request': self.request, 'team': team}
        serializer = JoinTeamSerializer(data=request.data, context=context)

        if team:
            # User CAN join team
            if serializer.is_valid():
                try:
                    team.members.add(user.player)                    
                    return Response({'status': 'joined team'})
        
                except user._meta.model.player.RelatedObjectDoesNotExist:
                    pass            
                
        return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['get'], detail=True,
        permission_classes=[permissions.CanReadTeam],
        url_path='regenerate-invite-code'
    )
    def regenerate_invite_code(self, request, pk=None):
        team = Team.objects.filter(pk=pk).first()
        
        has_permission = can_regenerate_team_invite_code(team, request.user)
        
        if has_permission:
            new_invite_code = team.generate_invite_code()

            return Response(
                {
                    'status': 'invite code regenerated',
                    'invite_code': new_invite_code 
                }
            )
        return Response(
            {'error': 'permission denied'},
            status=status.HTTP_400_BAD_REQUEST
        )


class DynastyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Dynasty.objects.all().order_by('name').distinct()
    serializer_class = DynastySerializer
    filterset_class = DynastyFilter

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all().order_by('id')
    queryset = queryset.prefetch_related(
        Prefetch('teams', queryset=Team.objects.annotate(
            wins=Count('won_match_results', distinct=True)).annotate(losses=Count('lost_match_results', distinct=True))),
    )
    queryset = queryset.prefetch_related('teams__circuit__season')
    queryset = queryset.prefetch_related('aliases')
    queryset = queryset.prefetch_related('awards__stats')
    queryset = queryset.prefetch_related('awards__round')
    queryset = queryset.prefetch_related('awards__award_category')
    
    permission_classes = [permissions.CanReadPlayer|permissions.CanEditPlayer]
    http_method_names = ['get', 'put', 'patch', 'delete']
    serializer_class = PlayerSerializer
    filterset_class = PlayerFilter

class CasterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Caster.objects.all().order_by('player__name')
    queryset = queryset.select_related('player')
    filterset_class = CasterFilter

    serializer_class = CasterSerializer

class StreamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stream.objects.all().order_by('-start_time')
    serializer_class = StreamSerializer
    filterset_class = StreamFilter

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all().order_by('start_time')
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

