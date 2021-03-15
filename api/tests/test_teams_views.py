from pytest import mark
from teams.tests.factories import TeamFactory
from api.tests.services import BuzzClient
from leagues.tests.factories import CircuitFactory
from players.tests.factories import PlayerFactory


@mark.django_db
def test_get_teams_by_name(django_app):
    """
    Get teams by basic name filter.
    """
    client = BuzzClient(django_app)

    team = TeamFactory()
    TeamFactory()    
    
    params = f'name={team.name}'
    resp = client.teams(params=params)
    
    assert resp['count'] == 1
    entry = resp['results'][0]

    assert entry['id'] == team.id
    assert entry['name'] == team.name
    assert entry['captain']['id'] == team.captain.id
    assert entry['is_active'] == team.is_active
    assert len(entry['members']) == team.members.count()
    assert entry['can_add_members'] == team.can_add_members
    assert entry['wins'] == 0
    assert entry['losses'] == 0
    assert not 'invite_code' in entry.keys()

@mark.django_db
def test_get_team_detail(django_app):
    """
    Get team detail view by object id
    """
    client = BuzzClient(django_app)

    team = TeamFactory()
    TeamFactory()    

    params = f'name={team.name}'
    entry = client.team(team.id)
    
    assert entry['id'] == team.id
    assert entry['name'] == team.name
    assert entry['captain']['id'] == team.captain.id
    assert entry['is_active'] == team.is_active
    assert len(entry['members']) == team.members.count()
    assert entry['can_add_members'] == team.can_add_members
    assert entry['wins'] == team.win_count
    assert entry['losses'] == team.loss_count

    assert not entry['invite_code']

@mark.django_db
def test_get_team_detail_as_captain(django_app):
    """
    Get team detail view by object id as captain, to see special secret fields
    """
    team = TeamFactory()
    player = team.captain   
    client = BuzzClient(django_app, token=player.get_or_create_token())

    params = f'name={team.name}'
    entry = client.team(team.id)
    
    
    assert entry['invite_code'] == team.invite_code
    assert entry['name'] == team.name
    assert entry['captain']['id'] == team.captain.id
    assert entry['is_active'] == team.is_active
    assert len(entry['members']) == team.members.count()
    assert entry['can_add_members'] == team.can_add_members
    assert entry['wins'] == team.win_count
    assert entry['losses'] == team.loss_count

@mark.django_db
def test_create_team_permission_granted(django_app):
    """
    Create team object and get results
    """
    player = PlayerFactory()
    circuit = CircuitFactory()

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    data = {
        'name': 'My Dope Team',
        'circuit': circuit.id,
    }
    
    resp = client.teams(None, method='POST', data=data, expect_errors=True)
    team = resp.json
    
    assert team['name'] == data['name']
    assert team['circuit'] == data['circuit']
    assert team['captain']['id'] == player.id
    assert team['members'][0]['id'] == player.id

@mark.django_db
def test_create_team_registration_closed_permission_denied(django_app):
    """
    Can't create a team for a season that is closed
    """
    player = PlayerFactory()
    circuit = CircuitFactory()
    season = circuit.season
    season.is_active = False
    season.save()

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    data = {
        'name': 'My Dope Team',
        'circuit': circuit.id,
    }
    
    resp = client.teams(None, method='POST', data=data, expect_errors=True)

    assert resp.status_code == 400
    assert player.teams.all().count() == 0
    

@mark.django_db
def test_create_team_two_existing_team_permission_denied(django_app):
    """
    You can create two teams max per season.
    """
    player = PlayerFactory()
    west_circuit = CircuitFactory(region='W',  tier='1')
    season = west_circuit.season
    east_circuit = CircuitFactory(region='E', tier='1', season=season)
    all_circuit = CircuitFactory(region='A', tier='1', season=season)

    TeamFactory(captain=player, circuit=west_circuit)
    TeamFactory(captain=player, circuit=east_circuit)

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    data = {
        'name': 'My Third Team',
        'circuit': all_circuit.id,
    }
    
    resp = client.teams(None, method='POST', data=data, expect_errors=True)


    assert resp.status_code == 400
    assert player.teams.filter(captain=player).count() == 2

@mark.django_db
def test_create_team_existing_team_different_region_permission_granted(django_app):
    """
    You CAN create a second team in a season, if the region is DIFFERENT.
    """
    player = PlayerFactory()
    west_circuit = CircuitFactory(region='W',  tier='1')
    season = west_circuit.season
    east_circuit = CircuitFactory(region='E', tier='1', season=season)

    team = TeamFactory(circuit=west_circuit, captain=player)

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    data = {
        'name': 'My T1 East Team',
        'circuit': east_circuit.id,
    }
    
    resp = client.teams(None, method='POST', data=data, expect_errors=True)

    assert resp.status_code == 201
    assert player.teams.filter(captain=player).count() == 2
    
@mark.django_db
def test_create_team_existing_team_same_region_permission_denied(django_app):
    """
    You CAN'T create two teams in a season, IF their regions are the SAME.
    """
    player = PlayerFactory()
    west_circuit = CircuitFactory(region='W',  tier='1')
    season = west_circuit.season
    east_circuit = CircuitFactory(region='W', tier='2', season=season)

    team = TeamFactory(circuit=west_circuit, captain=player)

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    data = {
        'name': 'My T2 West Team',
        'circuit': west_circuit.id,
    }
    
    resp = client.teams(None, method='POST', data=data, expect_errors=True)

    assert resp.status_code == 400
    assert player.teams.filter(captain=player).count() == 1


@mark.django_db
def test_rename_team_as_captain_permission_granted(django_app):
    """
    Get team detail view by object id as captain, to see special secret fields
    """
    team = TeamFactory()
    player = team.captain   
    client = BuzzClient(django_app, token=player.get_or_create_token())

    data = {
        'name': 'My New Team Name',
    }

    entry = client.team(team.id, method='PATCH', data=data)
    assert entry['name'] == data['name']

    team.refresh_from_db()
    assert team.name == data['name']


@mark.django_db
def test_rename_team_as_captain_permission_granted_ignore_circuit(django_app):
    """
    Don't let a player change their circuit id in the patch update.
    """
    team = TeamFactory()
    player = team.captain   
    client = BuzzClient(django_app, token=player.get_or_create_token())

    other_circuit = CircuitFactory()

    data = {
        'name': 'My New Team Name',
        'ciruit': other_circuit.id
    }

    entry = client.team(team.id, method='PATCH', data=data)
    
    team.refresh_from_db()
    assert team.circuit != other_circuit


@mark.django_db
def test_rename_team_as_member_permission_denied(django_app):
    """
    Don't let a member of team rename the team!
    """
    team = TeamFactory()
    player = PlayerFactory()
    team.members.add(player)

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)

    data = {'name': 'My New Team Name'}
    resp = client.team(team.id, method='PATCH', data=data, expect_errors=True)
    
    assert resp.status_code == 403
    team.refresh_from_db()
    assert team.name != data['name']


@mark.django_db
def test_rename_team_as_rando_permission_denied(django_app):
    """
    Don't let a random person rename the team!
    """
    team = TeamFactory()
    player = PlayerFactory()

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)

    data = {'name': 'My New Team Name'}
    resp = client.team(team.id, method='PATCH', data=data, expect_errors=True)
    
    assert resp.status_code == 403
    team.refresh_from_db()
    assert team.name != data['name']
    
@mark.django_db
def test_join_team_permission_granted(django_app):
    """
    Join a team with a valid invite code, with no previous team memberships
    for season.
    """
    team = TeamFactory()
    player = PlayerFactory()

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    data = {
        'invite_code': team.invite_code
    }
    
    resp = client.join_team(team.id, method='POST', data=data, expect_errors=False)
    
    assert resp.status_code == 200
    assert team.members.filter(id=player.id).exists()


@mark.django_db
def test_join_team_existing_member_other_region_permission_granted(django_app):
    """
    Join a team with a valid invite code, have membership in another team 
    but it's in a different region.
    """
    west_circuit = CircuitFactory(region='W',  tier='1')
    season = west_circuit.season
    east_circuit = CircuitFactory(region='E', tier='1', season=season)

    west_team = TeamFactory(circuit=west_circuit)
    east_team = TeamFactory(circuit=east_circuit)
    
    player = west_team.members.first()

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    data = {
        'invite_code': east_team.invite_code
    }
    
    resp = client.join_team(
        east_team.id, method='POST', data=data, expect_errors=False)
    
    assert resp.status_code == 200
    assert east_team.members.filter(id=player.id).exists()

@mark.django_db
def test_join_team_invalid_invite_code_permission_denied(django_app):
    """
    Deny access to join team with invalid invite code.
    """
    team = TeamFactory()
    player = PlayerFactory()

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    data = {
        'invite_code': 'ABC123XY'
    }
    
    resp = client.join_team(team.id, method='POST', data=data, expect_errors=True)
    
    assert resp.status_code == 400
    assert not team.members.filter(id=player.id).exists()

@mark.django_db
def test_join_team_rosters_closed_permission_denied(django_app):
    """
    Deny access to join team when season rosters are closed
    """
    team = TeamFactory()
    season = team.circuit.season
    season.rosters_open = False
    season.save()

    player = PlayerFactory()

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    data = {
        'invite_code': team.invite_code
    }
    
    resp = client.join_team(team.id, method='POST', data=data, expect_errors=True)
    
    assert resp.status_code == 400
    assert not team.members.filter(id=player.id).exists()

@mark.django_db
def test_join_team_roster_maxed_permission_denied(django_app):
    """
    Deny access to join team when number of members on roster maxed out
    """
    team = TeamFactory(members=[
        PlayerFactory(), PlayerFactory(), PlayerFactory(), PlayerFactory(),
        PlayerFactory(), PlayerFactory()
    ])

    player = PlayerFactory()

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    data = {
        'invite_code': team.invite_code
    }
    
    resp = client.join_team(team.id, method='POST', data=data, expect_errors=True)
    
    assert resp.status_code == 400
    assert not team.members.filter(id=player.id).exists()

@mark.django_db
def test_join_team_player_has_two_teams_permission_denied(django_app):
    """
    Player can only be on two teams in a season, deny access to a third.
    """
    west_circuit = CircuitFactory(region='W',  tier='1')
    season = west_circuit.season
    east_circuit = CircuitFactory(season=season, region='E',  tier='1')
    third_circuit = CircuitFactory(season=season, region='E',  tier='2')

    west_team = TeamFactory(circuit=west_circuit)
    east_team = TeamFactory(circuit=east_circuit)
    
    third_team = TeamFactory(circuit=third_circuit)
    
    player = west_team.members.first()
    east_team.members.add(player)

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    data = {
        'invite_code': third_team.invite_code
    }
    
    resp = client.join_team(
        third_team.id, method='POST', data=data, expect_errors=True)
    
    assert resp.status_code == 400
    assert not third_team.members.filter(id=player.id).exists()


@mark.django_db
def test_join_team_player_has_team_in_same_region_permission_denied(django_app):
    """
    Player can only be on one team per region.
    """
    west_circuit_1 = CircuitFactory(region='W',  tier='1')
    season = west_circuit_1.season
    west_circuit_2 = CircuitFactory(season=season, region='W',  tier='2')

    west_team_1 = TeamFactory(circuit=west_circuit_1)
    west_team_2 = TeamFactory(circuit=west_circuit_2)
    
    player = west_team_1.members.first()

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    data = {
        'invite_code': west_team_2.invite_code
    }
    
    resp = client.join_team(
        west_team_2.id, method='POST', data=data, expect_errors=True)
    
    assert resp.status_code == 400
    assert not west_team_2.members.filter(id=player.id).exists()


@mark.django_db
def test_join_team_existing_member_permission_denied(django_app):
    """
    Cannot join a team if you already have are a member of the team.
    """
    team = TeamFactory()
    player = team.members.first()

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    data = {
        'invite_code': team.invite_code
    }
    
    resp = client.join_team(team.id, method='POST', data=data, expect_errors=True)
    
    assert resp.status_code == 400
    assert team.members.filter(id=player.id).count() == 1

@mark.django_db
def test_regenerate_team_invite_code_access_granted(django_app):
    """
    Generate a new invite code if requester is team captain.
    """
    team = TeamFactory()
    player = team.members.first()
    current_invite_code = team.invite_code 
    
    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
        
    resp = client.regenerate_invite_code(
        team.id, method='GET', expect_errors=False)
    
    assert resp.status_code == 200
    assert resp.json['invite_code'] != current_invite_code
    
    team.refresh_from_db()
    assert team.invite_code != current_invite_code

@mark.django_db
def test_regenerate_team_invite_code_access_denied(django_app):
    """
    Do NOT generate a new invite code if requester is not team captain.
    """
    team = TeamFactory()
    player = PlayerFactory()
    current_invite_code = team.invite_code 
    
    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
        
    resp = client.regenerate_invite_code(
        team.id, method='GET', expect_errors=True)
    
    assert resp.status_code == 400

    team.refresh_from_db()
    assert team.invite_code == current_invite_code