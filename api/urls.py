from django.urls import include, path
from rest_framework_nested import routers
from .views import (
    AwardViewSet, LeagueViewSet, SeasonViewSet, CircuitViewSet, MatchViewSet,
    TeamViewSet, DynastyViewSet, PlayerViewSet, EventViewSet, RoundViewSet,
    BracketViewSet, CasterViewSet, StreamViewSet, PlayingViewSet,
    ReleaseViewSet, MeViewSet)

router = routers.DefaultRouter()
router.register(r'leagues', LeagueViewSet, basename='leagues')
router.register(r'players', PlayerViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'dynasties', DynastyViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'awards', AwardViewSet)
router.register(r'casters', CasterViewSet)
router.register(r'streams', StreamViewSet)
router.register(r'events', EventViewSet)
router.register(r'playing', PlayingViewSet)
router.register(r'releases', ReleaseViewSet)
router.register(r'me', MeViewSet, basename='me')

leagues_router = routers.NestedSimpleRouter(router, r'leagues', lookup='league')
leagues_router.register(r'seasons', SeasonViewSet, basename='seasons')

seasons_router = routers.NestedSimpleRouter(leagues_router, r'seasons', lookup='season')
seasons_router.register(r'circuits', CircuitViewSet, basename='circuits')
seasons_router.register(r'rounds', RoundViewSet, basename='rounds')
seasons_router.register(r'brackets', BracketViewSet, basename='brackets')

circuits_router = routers.NestedSimpleRouter(seasons_router, r'circuits', lookup='circuit')
rounds_router = routers.NestedSimpleRouter(seasons_router, r'rounds', lookup='round')
brackets_router = routers.NestedSimpleRouter(seasons_router, r'brackets', lookup='bracket')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(leagues_router.urls)),
    path('', include(seasons_router.urls)),
    path('', include(circuits_router.urls)),
    path('', include(rounds_router.urls)),
    path('', include(brackets_router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
