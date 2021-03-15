from pytest import mark
from players.tests.factories import PlayerFactory
from teams.tests.factories import TeamFactory
from api.tests.services import BuzzClient
from buzz.tests.factories import UserFactory


@mark.django_db
def test_get_players_by_name(django_app):
    """
    Get basic player data by player name
    """
    client = BuzzClient(django_app)
    
    player = PlayerFactory()
    active_team = TeamFactory(members=[player])
    
    inactive_team = TeamFactory(members=[player])
    inactive_season = inactive_team.circuit.season
    inactive_season.is_active = False
    inactive_season.save()
    
    params = f'name={player.name}'
    resp = client.players(params=params)
    
    assert resp['count'] == 1
    entry = resp['results'][0]

    assert entry['id'] == player.id
    assert entry['name'] == player.name
    assert entry['name_phonetic'] == player.name_phonetic
    assert entry['pronouns'] == player.pronouns
    assert entry['discord_username'] == player.discord_username
    assert entry['twitch_username'] == player.twitch_username
    assert entry['bio'] == player.bio
    assert entry['emoji'] == player.emoji
    assert entry['avatar_url'] == player.avatar_url
    assert entry['teams']

    assert entry['teams'][0]['name'] == active_team.name
    assert entry['teams'][0]['is_active'] == True
    assert entry['teams'][0]['wins'] == 0
    assert entry['teams'][0]['losses'] == 0

    assert entry['teams'][1]['name'] == inactive_team.name
    assert entry['teams'][1]['is_active'] == False
    
    # Need to build this out once Award Factory is in place
    assert 'token' not in entry.keys()


@mark.django_db
def test_get_player_detail(django_app):
    """
    Get player detail view by object id
    """
    client = BuzzClient(django_app)
    
    player = PlayerFactory()
    active_team = TeamFactory(members=[player])
    
    inactive_team = TeamFactory(members=[player])
    inactive_season = inactive_team.circuit.season
    inactive_season.is_active = False
    inactive_season.save()
    
    entry = client.player(player.id)

    assert entry['id'] == player.id
    assert entry['name'] == player.name
    assert entry['name_phonetic'] == player.name_phonetic
    assert entry['pronouns'] == player.pronouns
    assert entry['discord_username'] == player.discord_username
    assert entry['twitch_username'] == player.twitch_username
    assert entry['bio'] == player.bio
    assert entry['emoji'] == player.emoji
    assert entry['avatar_url'] == player.avatar_url
    assert entry['teams']

    assert entry['teams'][0]['name'] == active_team.name
    assert entry['teams'][0]['is_active'] == True
    assert entry['teams'][0]['wins'] == 0
    assert entry['teams'][0]['losses'] == 0

    assert entry['teams'][1]['name'] == inactive_team.name
    assert entry['teams'][1]['is_active'] == False
    
    # Need to build this out once Award Factory is in place
    assert 'awards' in entry.keys()

    # Keep these out!
    assert 'token' not in entry.keys()

@mark.django_db
def test_update_player_permission_granted(django_app):
    """
    Update player info.
    """
    player = PlayerFactory()

    client = BuzzClient(django_app, player.get_or_create_token())
    
    data = {
        'pronouns': 'abc123',
        'name_phonetic': 'ohhh-kayyy',
        'twitch_username': 'bogus_',
        'bio': 'My new bio',
        'emoji': 'testmoji'
    }
    
    entry = client.player(player.id, method='PATCH', data=data)

    for k, v in data.items():
        assert entry[k] == v

@mark.django_db
def test_update_player_permission_granted_ignore_read_only_fields(django_app):
    """
    Don't let players update forbidden fields.
    """
    player = PlayerFactory()

    client = BuzzClient(django_app, token=player.get_or_create_token())
    
    data = {
        'id': '12345',
        'discord_username': 'admin'
    }
    
    entry = client.player(player.id, method='PATCH', data=data)
    
    for k,v in data.items():
        assert entry[k] != v

@mark.django_db
def test_update_player_permission_denied(django_app):
    """
    Deny access for players to update information for other players
    """
    player = PlayerFactory()
    bad_player = PlayerFactory()

    client = BuzzClient(
        django_app, token=bad_player.get_or_create_token(), return_json=False)
    
    data = {
        'pronouns': 'abc123',
        'name_phonetic': 'ohhh-kayyy',
        'twitch_username': 'bogus_',
        'bio': 'My new bio',
        'emoji': 'testmoji'
    }
    
    resp = client.player(player.id, method='PATCH', data=data, expect_errors=True)

    assert resp.status_code == 403

    for k, v in data.items():
        assert v != getattr(player, k)


@mark.django_db
def test_delete_player_self_permission_denied(django_app):
    """
    Player cannot delete themselves.
    """
    player = PlayerFactory()

    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    
    data = {
        'id': '12345',
        'discord_username': 'admin'
    }
    
    resp = client.player(player.id, method='DELETE', expect_errors=True) 
    assert resp.status_code == 403
    
    player.refresh_from_db()
    assert player.id
      
def test_create_player_permission_denied(django_app):
    """
    Player cannot create arbitrary additional Players.
    """
    player = PlayerFactory()
    
    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    data = {
        'name': 'misbehavin',
        'pronouns': 'abc123',
        'name_phonetic': 'ohhh-kayyy',
        'twitch_username': 'bogus_',
        'bio': 'My new bio',
        'emoji': 'testmoji'
    }
    
    resp = client.players(None, method='POST', data=data, expect_errors=True)
    assert resp.status_code == 405
