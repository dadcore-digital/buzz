from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from rest_framework.authtoken.models import Token
from players.services import connect_user_to_player

class Home(TemplateView):
    template_name = 'home.html'


class DispatchAfterLogin(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            token, created = Token.objects.get_or_create(user=request.user)

            player = connect_user_to_player(request.user)
            url = settings.BGL_AUTH_HANDOFF_URL + f'/?token={token}'
            return redirect(url)

        raise PermissionDenied

def trigger_error(request):
    """Used for testing error reporting to 3rd party logging services."""
    division_by_zero = 1 / 0
