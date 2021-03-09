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
    assert entry['wins'] == team.wins
    assert entry['losses'] == team.losses

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
    assert entry['wins'] == team.wins
    assert entry['losses'] == team.losses


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
    