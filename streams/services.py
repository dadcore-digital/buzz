import re
import requests
from django.conf import settings
from .models import Stream

class Twitch:
    
    def __init__(self):

        # Twitch Settings
        self.CLIENT_ID = settings.TWITCH_CLIENT_ID
        self.CLIENT_SECRET = settings.TWITCH_CLIENT_SECRET
        self.GAME_ID = settings.TWITCH_GAME_ID
        self.API_BASE = 'https://api.twitch.tv/helix'

    def get_access_token(self):
        """
        Use 
        """
        url ='https://id.twitch.tv/oauth2/token'
        data = {
                'client_id': self.CLIENT_ID,
                'client_secret': self.CLIENT_SECRET,
                'grant_type': 'client_credentials',
                'scope': ''
        }
        req = requests.post(url, data, timeout=120)
        access_token = req.json()['access_token']
                
        return access_token

    def get_live_streams(self, timeout=120):
        """Get a list of all live twitch streams for KQB."""

        params = {'game_id': self.GAME_ID}        
        access_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Client-ID': self.CLIENT_ID
        }
        resp = requests.get(
            f'{self.API_BASE}/streams', params=params, headers=headers, timeout=timeout)
        
        if resp.status_code == 200:
            streams = resp.json()['data']
            return streams                
        
        # Access token has expired, at least set it up for next time to work
        elif resp.status_code == 401:
            return None
        
        return None

def update_twitch_streams(timeout=120):
    """
    Update database with live Twitch streams for game.
    """
    tw = Twitch()
    results = tw.get_live_streams(timeout=timeout)
    created = 0
    streams = []
    live_stream_ids = []

    for entry in results:
        stream, created = Stream.objects.get_or_create(
            stream_id=entry['id'], start_time = entry['started_at'])
        stream.twitch_id = entry['id']
        stream.user_id = entry['user_id']
        stream.username = entry['user_name'],
        stream.name = entry['title']
        stream.start_time = entry['started_at']
        stream.thumbnail_url = entry['thumbnail_url']
        current_view_count = entry['viewer_count']

        if entry['type'] == 'live':
            stream.is_live = True

        if current_view_count > stream.max_viewer_count:
            stream.max_viewer_count = current_view_count
        
        stream.save()
        streams.append(stream)
        live_stream_ids.append(stream.id)
        

        if created:
            created +=1
    
    # Set all streams no in results to is_live = False
    marked_offline = Stream.objects.filter(is_live=True).exclude(id__in=live_stream_ids).update(is_live=False)

    return {
        'total': len(streams),
        'updated': len(streams) - created,
        'created': created,
        'marked_offline': marked_offline
    }



