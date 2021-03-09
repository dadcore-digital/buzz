from pytest import mark
from teams.tests.factories import TeamFactory
from api.tests.services import BuzzClient

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
