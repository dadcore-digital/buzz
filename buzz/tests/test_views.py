from pytest import mark
from players.models import Player
from players.tests.factories import IGLPlayerLookupFactory, PlayerFactory
from buzz.tests.factories import UserFactory, SocialAccountFactory

@mark.django_db
def test_discord_login_page(django_app):
    """
    Discord login should be a static page with text 'Buzz API' and a login link
    """
    resp = django_app.get('/login/')
    resp.mustcontain('Buzz API')


@mark.django_db
def test_dispatch_create_player(django_app):
    """
    Sign up with a new Player object.

    We assume AllAuth + Discord has handed us a valid User object
    """
    igl_lookup = IGLPlayerLookupFactory()
    SocialAccountFactory(
        user=UserFactory(), uid=igl_lookup.discord_uid)
    
    # Not associated with above user data
    social_account = SocialAccountFactory()
    user = social_account.user

    resp = django_app.get('/dispatch/', user=user)  

    assert resp.status_code == 302
    resp = resp.follow()
    
    assert resp.request.path == '/'

    assert Player.objects.count() == 1
    
    player = Player.objects.first()
    assert user.player == player


@mark.django_db
def test_dispatch_login_has_user_has_player(django_app):
    """
    Sign in a user with an existing account and player object

    We assume AllAuth + Discord has handed us a valid User object
    """
    social_account = SocialAccountFactory()
    user = social_account.user
    player = PlayerFactory(user=user)

    resp = django_app.get('/dispatch/', user=user)  

    assert resp.status_code == 302
    resp = resp.follow()
    
    assert resp.request.path == '/'

    assert Player.objects.count() == 1
    
    player = Player.objects.first()
    assert user.player == player

    
@mark.django_db
def test_dispatch_create_player_has_historical_player_object(django_app):
    """
    Sign up with a new Player object has old IGL player object in database.

    We assume AllAuth + Discord has handed us a valid User object
    """
    igl_lookup = IGLPlayerLookupFactory()
    social_account = SocialAccountFactory(
        user=UserFactory(), uid=igl_lookup.discord_uid)
    player = PlayerFactory(name=igl_lookup.igl_player_name)
    player.user = None
    player.save()
    
    user = social_account.user
    resp = django_app.get('/dispatch/', user=user)  

    assert resp.status_code == 302
    resp = resp.follow()

    assert resp.request.query_string == f'token={user.player.get_or_create_token().key}&new_signup=true&connected_user_to_player=true&connected_player_name={player.name}'

    player.refresh_from_db()
    assert user.player == player


@mark.django_db
def test_dispatch_create_player_conflicting_player_object(django_app):
    """
    Sign up as a new Player when another user has the same Player name.

    In this case we append a number three digit number to the end of the
    player name.
    """
    social_account = SocialAccountFactory()
    existing_player = PlayerFactory(user=social_account.user)

    social_account = SocialAccountFactory()
    user = social_account.user

    # Existing player renames themselves to match another incoming player
    existing_player.name = user.username
    existing_player.save()
    resp = django_app.get('/dispatch/', user=user)  
    resp = resp.follow()

    assert resp.request.query_string == f'token={user.player.get_or_create_token().key}&new_signup=true'
    assert existing_player.name == user.player.name[:-3]
