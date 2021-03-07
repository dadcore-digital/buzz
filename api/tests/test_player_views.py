from pytest import mark
from players.tests.factories import PlayerFactory
from teams.tests.factories import TeamFactory
from api.tests.services import BuzzClient

@mark.django_db
def test_get_player_by_name(django_app):
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
    resp = client.players(params)
    
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
    assert 'award_summary' in entry.keys()
