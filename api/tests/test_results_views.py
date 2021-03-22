from pytest import mark
from matches.tests.factories import MatchFactory, ResultFactory
from players.tests.factories import PlayerFactory
from teams.tests.factories import TeamFactory
from api.tests.services import BuzzClient

@mark.django_db
def test_create_result_permission_granted(django_app):
    """
    Create Result object for Match.
    """
    match = MatchFactory()
    player = match.home.captain
    
    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    data = {
        'match': match.id,
        'status': 'C',
        'winner': match.home.id,
        'loser': match.away.id,
        'sets': [
            { 'number': 1, 'winner': match.away.id, 'loser': match.home.id },
            { 'number': 2, 'winner': match.away.id, 'loser': match.home.id },
            { 'number': 3, 'winner': match.home.id, 'loser': match.away.id },
            { 'number': 4, 'winner': match.home.id, 'loser': match.away.id },
            { 'number': 5, 'winner': match.home.id, 'loser': match.away.id },

        ]
    }
    
    resp = client.results(None, method='POST', data=data, expect_errors=False)
    
    assert resp.status_code == 302
    resp = resp.follow()

    match.refresh_from_db()
    result = resp.json
    assert result['winner'] == match.home.id
    assert result['loser'] == match.away.id

    assert result['sets'][0]['number'] == 1
    assert result['sets'][1]['number'] == 2
    assert result['sets'][2]['number'] == 3
    assert result['sets'][3]['number'] == 4
    assert result['sets'][4]['number'] == 5

    assert result['sets'][0]['winner'] == match.away.id
    assert result['sets'][1]['winner'] == match.away.id
    assert result['sets'][2]['winner'] == match.home.id
    assert result['sets'][3]['winner'] == match.home.id
    assert result['sets'][4]['winner'] == match.home.id

    assert result['sets'][0]['loser'] == match.home.id
    assert result['sets'][1]['loser'] == match.home.id
    assert result['sets'][2]['loser'] == match.away.id
    assert result['sets'][3]['loser'] == match.away.id
    assert result['sets'][4]['loser'] == match.away.id


@mark.django_db
def test_create_result_with_log_permission_granted(django_app):
    """
    Create Result object for Match and include raw log data for each set.
    """
    match = MatchFactory()
    player = match.home.captain
    
    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    data = {
        'match': match.id,
        'status': 'C',
        'winner': match.home.id,
        'loser': match.away.id,
        'sets': [
            {
                'number': 1,
                'winner': match.away.id,
                'loser': match.home.id,
                'log': {
                    'filename': 'myfilename1.json',
                    'body': '{"results": "yadayada"}'
                }
            },
            {
                'number': 2,
                'winner': match.away.id,
                'loser': match.home.id,
                'log': {
                    'filename': 'myfilename2.json',
                    'body': '{"results": "okaygreat"}'
                }
            },
            {
                'number': 3,
                'winner': match.away.id,
                'loser': match.home.id,
                'log': {
                    'filename': 'myfilename3.json',
                    'body': '{"results": "morestuff"}'
                }
            }
        ]
    }
    
    resp = client.results(None, method='POST', data=data, expect_errors=True)
    assert resp.status_code == 302
    resp = resp.follow()

    assert resp.json['sets'][0]['log']['filename'] == 'myfilename1.json'
    assert resp.json['sets'][0]['log']['body'] == '{"results": "yadayada"}'

@mark.django_db
def test_create_result_not_captain_permission_denied(django_app):
    """
    Don't allow non-team captains to submit match results
    """
    match = MatchFactory()
    player = PlayerFactory()
    
    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    # This data is valid
    data = {
        'match': match.id,
        'status': 'C',
        'winner': match.home.id,
        'loser': match.away.id,
        'sets': [
            { 'number': 1, 'winner': match.away.id, 'loser': match.home.id },
            { 'number': 2, 'winner': match.away.id, 'loser': match.home.id },
            { 'number': 3, 'winner': match.home.id, 'loser': match.away.id },
            { 'number': 4, 'winner': match.home.id, 'loser': match.away.id },
            { 'number': 5, 'winner': match.home.id, 'loser': match.away.id },

        ]
    }

    resp = client.results(None, method='POST', data=data, expect_errors=True)
    assert resp.status_code == 400
    assert resp.json['non_field_errors'][0] == 'Permission Error: Only team captains can submit match results.'
    
    match.refresh_from_db()
    assert not hasattr(match, 'result')
    

@mark.django_db
def test_create_result_has_result_permission_denied(django_app):
    """
    Can't submit a Result if one already exists.
    """
    result = ResultFactory()
    match = result.match
    player = match.home.captain
    
    result_id = result.id
    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    # This data is valid
    data = {
        'match': match.id,
        'status': 'C',
        'winner': match.home.id,
        'loser': match.away.id,
        'sets': [
            { 'number': 1, 'winner': match.away.id, 'loser': match.home.id },
            { 'number': 2, 'winner': match.away.id, 'loser': match.home.id },
            { 'number': 3, 'winner': match.home.id, 'loser': match.away.id },
            { 'number': 4, 'winner': match.home.id, 'loser': match.away.id },
            { 'number': 5, 'winner': match.home.id, 'loser': match.away.id },

        ]
    }

    resp = client.results(None, method='POST', data=data, expect_errors=True)
    assert resp.status_code == 400

    match.refresh_from_db()
    assert match.result.id == result_id

@mark.django_db
def test_create_result_not_enough_sets_permission_denied(django_app):
    """
    Must submit at least 3 sets in match.
    """
    match = MatchFactory()
    player = match.home.captain
    
    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    # This data is valid
    data = {
        'match': match.id,
        'status': 'C',
        'winner': match.home.id,
        'loser': match.away.id,
        'sets': [
            { 'number': 1, 'winner': match.away.id, 'loser': match.home.id }

        ]
    }

    resp = client.results(None, method='POST', data=data, expect_errors=True)
    assert resp.status_code == 400
    assert resp.json['non_field_errors'][0] == 'Validation Error: You must include results for at least three Sets.'

    match.refresh_from_db()
    assert not hasattr(match, 'result')
    

@mark.django_db
def test_create_result_too_many_sets_permission_denied(django_app):
    """
    Must submit n more than 5 sets in match.
    """
    match = MatchFactory()
    player = match.home.captain
    
    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    # This data is valid
    data = {
        'match': match.id,
        'status': 'C',
        'winner': match.home.id,
        'loser': match.away.id,
        'sets': [
            { 'number': 1, 'winner': match.away.id, 'loser': match.home.id },
            { 'number': 2, 'winner': match.away.id, 'loser': match.home.id },
            { 'number': 3, 'winner': match.away.id, 'loser': match.home.id },
            { 'number': 4, 'winner': match.away.id, 'loser': match.home.id },
            { 'number': 5, 'winner': match.away.id, 'loser': match.home.id },
            { 'number': 6, 'winner': match.away.id, 'loser': match.home.id }

        ]
    }

    resp = client.results(None, method='POST', data=data, expect_errors=True)
    assert resp.status_code == 400
    assert resp.json['non_field_errors'][0] == 'Validation Error: You cannot include more than five Sets.'

    match.refresh_from_db()
    assert not hasattr(match, 'result')


@mark.django_db
def test_create_result_winner_must_be_match_team_permission_denied(django_app):
    """
    Winner of Result must either be Match.home or Match.away
    """
    match = MatchFactory()
    player = match.home.captain
    
    bogus_team = TeamFactory()
    
    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    # This data is valid
    data = {
        'match': match.id,
        'status': 'C',
        'winner': bogus_team.id,
        'loser': match.away.id,
        'sets': [
            { 'number': 1, 'winner': match.away.id, 'loser': match.home.id },
            { 'number': 2, 'winner': match.away.id, 'loser': match.home.id },
            { 'number': 3, 'winner': match.away.id, 'loser': match.home.id },
        ]
    }

    resp = client.results(None, method='POST', data=data, expect_errors=True)

    assert resp.status_code == 400
    assert resp.json['non_field_errors'][0] == 'Validation Error: Result Winner and Loser must be associated with Match'

    match.refresh_from_db()
    assert not hasattr(match, 'result')

@mark.django_db
def test_create_result_loser_must_be_match_team_permission_denied(django_app):
    """
    Loser of Result must either be Match.home or Match.away
    """
    match = MatchFactory()
    player = match.home.captain
    
    bogus_team = TeamFactory()
    
    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    # This data is valid
    data = {
        'match': match.id,
        'status': 'C',
        'winner': match.home.id,
        'loser': bogus_team.id,
        'sets': [
            { 'number': 1, 'winner': match.away.id, 'loser': match.home.id },
            { 'number': 2, 'winner': match.away.id, 'loser': match.home.id },
            { 'number': 3, 'winner': match.away.id, 'loser': match.home.id },
        ]
    }

    resp = client.results(None, method='POST', data=data, expect_errors=True)

    assert resp.status_code == 400
    assert resp.json['non_field_errors'][0] == 'Validation Error: Result Winner and Loser must be associated with Match'

    match.refresh_from_db()
    assert not hasattr(match, 'result')

@mark.django_db
def test_create_result_set_winner_must_be_match_team_permission_denied(django_app):
    """
    Winner of all Sets must either be Match.home or Match.away
    """
    match = MatchFactory()
    player = match.home.captain
    
    bogus_team = TeamFactory()
    
    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    # This data is valid
    data = {
        'match': match.id,
        'status': 'C',
        'winner': match.home.id,
        'loser': match.away.id,
        'sets': [
            { 'number': 1, 'winner': bogus_team.id, 'loser': match.home.id },
            { 'number': 2, 'winner': match.away.id, 'loser': match.home.id },
            { 'number': 3, 'winner': match.away.id, 'loser': match.home.id },
        ]
    }

    resp = client.results(None, method='POST', data=data, expect_errors=True)

    assert resp.status_code == 400
    assert resp.json['non_field_errors'][0] == 'Validation Error: Set Winner and Loser must be associated with Match'

    match.refresh_from_db()
    assert not hasattr(match, 'result')


@mark.django_db
def test_create_result_set_loser_must_be_match_team_permission_denied(django_app):
    """
    Loser of all Sets must either be Match.home or Match.away
    """
    match = MatchFactory()
    player = match.home.captain
    
    bogus_team = TeamFactory()
    
    client = BuzzClient(
        django_app, token=player.get_or_create_token(), return_json=False)
    
    # This data is valid
    data = {
        'match': match.id,
        'status': 'C',
        'winner': match.home.id,
        'loser': match.away.id,
        'sets': [
            { 'number': 1, 'winner': match.away.id, 'loser': bogus_team.id },
            { 'number': 2, 'winner': match.away.id, 'loser': match.home.id },
            { 'number': 3, 'winner': match.away.id, 'loser': match.home.id },
        ]
    }

    resp = client.results(None, method='POST', data=data, expect_errors=True)

    assert resp.status_code == 400
    assert resp.json['non_field_errors'][0] == 'Validation Error: Set Winner and Loser must be associated with Match'

    match.refresh_from_db()
    assert not hasattr(match, 'result')
