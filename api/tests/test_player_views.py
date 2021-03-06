from pytest import mark
from players.tests.factories import PlayerFactory

@mark.django_db
def test_get_player_by_name(django_app):
    """
    Get basic player data by player name
    """
    player = PlayerFactory()
    params = f'name={player.name}'
    
    resp = django_app.get(f'/api/players/?{params}&format=json').json
    
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
