from django.urls import include, path
from rest_framework import routers
from .views import (
    AwardViewSet, LeagueViewSet, SeasonViewSet, CircuitViewSet, MatchViewSet,
    TeamViewSet, DynastyViewSet, PlayerViewSet, EventViewSet, RoundViewSet,
    CasterViewSet, StreamViewSet, PlayingViewSet, ReleaseViewSet,
    ResultViewSet, SetViewSet, MeViewSet, GameViewSet)

router = routers.DefaultRouter()
router.register(r'awards', AwardViewSet)
router.register(r'casters', CasterViewSet)
router.register(r'circuits', CircuitViewSet, basename='circuits')
router.register(r'dynasties', DynastyViewSet)
router.register(r'events', EventViewSet)
router.register(r'games', GameViewSet),
router.register(r'leagues', LeagueViewSet, basename='leagues')
router.register(r'matches', MatchViewSet)
router.register(r'me', MeViewSet, basename='me')
router.register(r'players', PlayerViewSet)
router.register(r'playing', PlayingViewSet)
router.register(r'results', ResultViewSet, basename='results'),
router.register(r'releases', ReleaseViewSet)
router.register(r'sets', SetViewSet),
router.register(r'rounds', RoundViewSet, basename='rounds')
router.register(r'streams', StreamViewSet)
router.register(r'seasons', SeasonViewSet, basename='seasons')
router.register(r'teams', TeamViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
