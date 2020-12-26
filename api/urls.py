from django.urls import include, path
from rest_framework_nested import routers
from .views import (
    AwardViewSet, LeagueViewSet, SeasonViewSet, CircuitViewSet, MatchViewSet,
    TeamViewSet, PlayerViewSet, EventViewSet, RoundViewSet)

router = routers.DefaultRouter()
router.register(r'awards', AwardViewSet)
router.register(r'rounds', RoundViewSet)
router.register(r'circuits', CircuitViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'events', EventViewSet)

router.register(r'leagues', LeagueViewSet)

leagues_router = routers.NestedSimpleRouter(router, r'leagues', lookup='league')
leagues_router.register(r'seasons', SeasonViewSet, basename='league-seasons')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(leagues_router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
