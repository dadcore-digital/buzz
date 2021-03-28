from pytest import mark
from dateutil import parser
from django.utils import timezone
from datetime import datetime, timedelta
from casters.tests.factories import CasterFactory
from players.tests.factories import PlayerFactory
from leagues.tests.factories import CircuitFactory
from matches.tests.factories import MatchFactory, ResultFactory
from api.tests.services import BuzzClient

@mark.filterwarnings(
    'ignore:DateTimeField Match.start_time received a naive datetime')
@mark.django_db
def test_get_matches_upcoming(django_app):
    """
    Get all upcmoing matches in next 24 hours
    """
    client = BuzzClient(django_app)
    circuit = CircuitFactory()

    now = timezone.now()
    match_1 = MatchFactory(circuit=circuit, start_time=now + timedelta(hours=2))
    match_2 = MatchFactory(circuit=circuit, start_time=now + timedelta(hours=23))

    # These should not show up in results
    MatchFactory(circuit=circuit, start_time=now + timedelta(hours=26))
    MatchFactory(circuit=circuit, start_time=now - timedelta(hours=1))

    params = 'hours=24'
    resp = client.matches(params)    

    assert resp['count'] == 2

    matches = resp['results']

    # Sort Order
    assert parser.parse(matches[0]['start_time']) < parser.parse(matches[1]['start_time'])
    
    # Basic field presence check
    assert matches[0]['home']['id'] == match_1.home.id
    assert matches[0]['away']['id'] == match_1.away.id
    assert matches[0]['circuit']
    assert matches[0]['round']
    assert 'number' in matches[0]['round'].keys()
    assert 'name' in matches[0]['round'].keys()
    assert matches[0]['start_time']
    assert matches[0]['time_until']
    assert matches[0]['scheduled']

    assert 'primary_caster' in matches[0].keys()
    assert 'secondary_casters' in matches[0].keys()
    assert 'result' in matches[0].keys()
    assert 'vod_link' in matches[0].keys()


@mark.django_db
def test_get_team_matches(django_app):
    """
    Get all upcmoing matches in next 24 hours
    """
    client = BuzzClient(django_app)
    circuit = CircuitFactory()

    now = timezone.now()

    match_1 = MatchFactory(circuit=circuit, start_time=now - timedelta(days=2))
    team = match_1.home 
    
    match_2 = MatchFactory(
        circuit=circuit, away=team, start_time=now + timedelta(hours=2)) 
    match_3 = MatchFactory(
        circuit=circuit, home=team, start_time=now + timedelta(days=8))
    match_4 = MatchFactory(
        circuit=circuit, away=team, start_time=now + timedelta(days=17))

    # These should not show up in results
    MatchFactory(circuit=circuit, start_time=now + timedelta(hours=26))
    MatchFactory(circuit=circuit, start_time=now - timedelta(hours=1))

    params = f'team={team.name}&league={circuit.season.league.name}&season={circuit.season.name}'
    resp = client.matches(params)    

    assert resp['count'] == 4

@mark.django_db
def test_get_matches_starts_in_minutes(django_app):
    """
    Get matches starting in the next n minutes
    """
    client = BuzzClient(django_app)
    circuit = CircuitFactory()

    now = timezone.now()

    match = MatchFactory(circuit=circuit, start_time=now + timedelta(minutes=5))
    
    MatchFactory(
        circuit=circuit, start_time=now + timedelta(minutes=7)) 

    MatchFactory(
        circuit=circuit, start_time=now - timedelta(minutes=1))

    params = 'starts_in_minutes=5'
    resp = client.matches(params)    

    assert resp['count'] == 1


@mark.django_db
def test_update_match_time_no_start_time_home_catapin_permission_granted(django_app):
    """
    Update match time as home team captain for a match that does not have yet
    have a start time.
    """
    now = timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    match = MatchFactory(start_time=None)
    
    player = match.home.captain

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    data = {'start_time': now }
    resp = client.match(match.id, method='PATCH', data=data)

    assert resp.status_code == 200
    
    entry = resp.json
    assert entry['start_time'] == now

@mark.django_db
def test_update_caster_no_existing_caster_permission_granted(django_app):
    """
    Update caster as home team captain when none has been set.
    """
    start_time = (
        timezone.now() + timedelta(hours=23)).strftime('%Y-%m-%dT%H:%M:%SZ')

    match = MatchFactory(start_time=start_time)    
    player = match.home.captain

    caster = CasterFactory()

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    data = {'primary_caster': caster.id }
    resp = client.match(match.id, method='PATCH', data=data)

    assert resp.status_code == 200
    
    entry = resp.json
    assert entry['primary_caster']['id'] == caster.id

@mark.django_db
def test_update_caster_has_existing_caster_permission_granted(django_app):
    """
    Update caster as home team captain when existing caster has been set.
    """
    old_caster = CasterFactory()
    new_caster = CasterFactory()

    start_time = (
        timezone.now() + timedelta(hours=23)).strftime('%Y-%m-%dT%H:%M:%SZ')

    match = MatchFactory(start_time=start_time, primary_caster=old_caster)  
    player = match.home.captain

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    data = {'primary_caster': new_caster.id }
    resp = client.match(match.id, method='PATCH', data=data)

    assert resp.status_code == 200
    
    entry = resp.json
    assert entry['primary_caster']['id'] == new_caster.id
    match.refresh_from_db()
    assert match.primary_caster == new_caster


@mark.django_db
def test_update_caster_team_member_permission_denied(django_app):
    """
    Raise permission denied when trying to update a caster as non-captain.
    """

    start_time = (
        timezone.now() + timedelta(hours=23)).strftime('%Y-%m-%dT%H:%M:%SZ')

    match = MatchFactory(start_time=start_time)  

    player = PlayerFactory()
    home = match.home
    home.members.add(player)

    caster = CasterFactory()

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    data = {'primary_caster': caster.id }
    resp = client.match(match.id, method='PATCH', data=data, expect_errors=True)

    assert resp.status_code == 403
    
    assert resp.json['detail'] == 'You do not have permission to perform this action.'
    
    match.refresh_from_db()
    assert not match.primary_caster

@mark.django_db
def test_update_match_time_no_start_time_away_catapin_permission_granted(django_app):
    """
    Update match time for a match as away team catapin that does not have yet
    have a start time.
    """
    now = timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    match = MatchFactory(start_time=None)
    
    player = match.away.captain

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    data = {'start_time': now }
    resp = client.match(match.id, method='PATCH', data=data)

    assert resp.status_code == 200
    
    entry = resp.json
    assert entry['start_time'] == now


@mark.django_db
def test_update_match_time_has_start_time_permission_granted(django_app):
    """
    Update match time for a match that DOES have a start time.
    """
    start_time = (
        timezone.now() + timedelta(hours=23)).strftime('%Y-%m-%dT%H:%M:%SZ')

    match = MatchFactory()
    
    player = match.home.captain

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)

    data = {'start_time': start_time }
    resp = client.match(match.id, method='PATCH', data=data)

    assert resp.status_code == 200
    
    entry = resp.json
    assert entry['start_time'] == start_time


@mark.django_db
def test_update_match_time_team_member_permission_denied(django_app):
    """
    A non-captain cannot update the match start time
    """
    now = timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    match = MatchFactory(start_time=None)
    
    player = PlayerFactory()
    home = match.home
    home.members.add(player)

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    data = {'start_time': now }
    resp = client.match(match.id, method='PATCH', data=data, expect_errors=True)

    assert resp.status_code == 403

    match.refresh_from_db()
    assert not match.start_time
    
@mark.django_db
def test_update_match_time_rando_permission_denied(django_app):
    """
    A random person cannot update the match start time
    """
    now = timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    match = MatchFactory(start_time=None)
    
    player = PlayerFactory()

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    data = {'start_time': now }
    resp = client.match(match.id, method='PATCH', data=data, expect_errors=True)

    assert resp.status_code == 403

    match.refresh_from_db()
    assert not match.start_time
    
@mark.django_db
def test_update_match_time_season_inactive_permission_denied(django_app):
    """
    Can't update match time for a match whose season is inactive.
    """
    match = MatchFactory(start_time=None)
    season = match.circuit.season
    season.is_active = False
    season.save()

    current_start_time = match.start_time
    new_start_time = timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    player = match.home.captain

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    data = {'start_time': new_start_time }
    resp = client.match(match.id, method='PATCH', data=data, expect_errors=True)

    assert resp.status_code == 403
    
    match.refresh_from_db() 
    assert match.start_time == current_start_time

@mark.django_db
def test_update_match_time_has_result_permission_denied(django_app):
    """
    Can't update match time for a match that already has a result.
    """
    result = ResultFactory()
    match = result.match

    current_start_time = match.start_time
    new_start_time = timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    player = match.home.captain

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    data = {'start_time': new_start_time }
    resp = client.match(match.id, method='PATCH', data=data, expect_errors=True)

    assert resp.status_code == 403
    
    match.refresh_from_db() 
    assert match.start_time == current_start_time

