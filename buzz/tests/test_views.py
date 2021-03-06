from pytest import mark

@mark.django_db
def test_homepage(django_app):
    """
    Homepage should be a static page with text 'Buzz API'
    """
    resp = django_app.get('/')
    resp.mustcontain('Buzz API')

