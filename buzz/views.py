from random import randint
from django.conf import settings
from django.db import IntegrityError, transaction
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from rest_framework.authtoken.models import Token
from players.models import Player
from players.services import connect_user_to_player

class Home(TemplateView):
    template_name = 'home.html'


class DispatchAfterLogin(View):
    def get(self, request, *args, **kwargs):

        new_signup = False
        connected_user_to_player = False

        if not request.user.is_anonymous:
            token, created = Token.objects.get_or_create(user=request.user)

            # Connect user to player object if not already connected
            if not hasattr(request.user, 'player'):
                new_signup = True
                player = connect_user_to_player(request.user)
            
                if player:
                    connected_user_to_player = True
                else:
                    try:
                        
                        # transaction.atomic is integration testing quirk,
                        # needed for test to run.
                        with transaction.atomic():
                            player = Player.objects.create(
                                name=request.user.username,
                                user=request.user
                            )
                    # Add random ints to end of name of conflicting player name
                    # encountered.
                    except IntegrityError:
                        player = Player.objects.create(
                            name=f'{request.user.username}{randint(100,999)}',
                            user=request.user
                        )
            else:
                player = request.user.player
                
            # Update player profile data from discord social account
            player.avatar_url = player.discord_avatar_url
            player.discord_username = player.discord_login_username
            player.save()

            url = settings.BGL_AUTH_HANDOFF_URL + f'/?token={token}'
            
            if new_signup:
                url += f'&new_signup=true'

            if connected_user_to_player:
                url += f'&connected_user_to_player=true&connected_player_name={player.name}'

            return redirect(url)

        raise PermissionDenied

def trigger_error(request):
    """Used for testing error reporting to 3rd party logging services."""
    division_by_zero = 1 / 0
