import requests
from django.conf import settings
from .models import Playing

class Steam:
    
    def __init__(self):
        

        self.GAME_ID = settings.STEAM_GAME_ID
        self.API_BASE = 'http://api.steampowered.com'
    
    def get_playing_count(self, simulate=False, timeout=120):
        """Get a count all people playing KQB on Steam currently."""
        
        params = {'appid': self.GAME_ID}
        api_path = f'ISteamUserStats/GetNumberOfCurrentPlayers/v0001/?appid={self.GAME_ID}'
        resp = requests.get(
            f'{self.API_BASE}/{api_path}', params=params, timeout=timeout)
        
        if resp.status_code == 200:
            return resp.json()['response']['player_count']
        
        return None


def update_steam_playing_count(timeout=120):
    """
    Update database with number of people currently playing game in steam.
    """
    steam = Steam()
    playing_count = steam.get_playing_count(timeout=timeout)
    obj = None

    if playing_count:
        obj = Playing.objects.create(total=playing_count)

    return obj