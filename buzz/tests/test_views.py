from pytest import mark

@mark.django_db
def test_discord_login_page(django_app):
    """
    Discord login should be a static page with text 'Buzz API' and a login link
    """
    resp = django_app.get('/login/')
    resp.mustcontain('Buzz API')

