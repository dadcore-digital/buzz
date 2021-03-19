import csv
import json
from django.db import IntegrityError
from players.models import Player, Alias, IGLPlayerLookup

def connect_user_to_player(user):
    """
    Connect a User object to an existing Player object.

    For players who have existing Player objects in the system, but are
    signing up as new users with Discord, we want them to have historical
    access to their Player object, and not create a dupe one.
    """
    social_account = user.socialaccount_set.all().first()

    if social_account:
        
        igl_player = IGLPlayerLookup.objects.filter(
            discord_uid=social_account.uid).first()
        
        if igl_player:
            
            # Try looking up by IGL PLayer Name first
            player = Player.objects.filter(
                name__iexact=igl_player.igl_player_name).first()

            # Then try by discord username
            if not player:
                player = Player.objects.filter(
                    discord_username__iexact=igl_player.discord_username).first()
            
            if player:
                player.user = user
                player.save()
            return player
    
    return None

def import_igl_discord_player_data(
    json_file_path, clear_igl_lookup_table=False, update_player_avatars=False):
    """
    Update IGLPlayerLookup table with list of IGL playernames and Discord Users.

    Takes a JSON file of IGL players names in the following format:

    {
        "id": 393937783783782378,
        "username": "gameplayer#9324",
        "avatar_url": "https://cdn.discordapp.com/avatars/393937783783782378/c7c1e03edd089663c0f6f7bfd35028b6.webp?size=1024",
        "nick": "playsgames!",
        "iglname": "GamePlayer"
    }

    ...and populate the IGLLookup table.

    Additionally, if update_player_avatars is passed in, will find any
    existing Player objects whose avatar is not already set, and if their
    Player.discord_username matches an entry in the JSON file, update their
    avatar accordingly.
    
    This should be a one-time thing, but useful to know how to have it on 
    record if we ever have to do a re-import for some reason. 

    Arguments:
    json_file_path -- A relative or full filepath to the JSON file to import.
    clear_igl_lookup_table -- If True, will delete all existing IGLPlayerLookup
                              objects in database. (bool) (optional)
    update_player_avatars -- If True will attempt to find existing Player
                            objects, even those not connected to a User
                            account, and assign avatars to them. (bool)
                            (optional)
    """
    with open(json_file_path) as f:
        users = json.load(f)
    
    if clear_igl_lookup_table:
        IGLPlayerLookup.objects.all().delete()

    for user in users:
        if (
            'id' in user.keys()
        ):
            igl_player = IGLPlayerLookup()

            # Some discord users we have in file have no associated IGL
            # name, but may have a player object none the less. We can
            # still associate them to their Player object via their 
            # discord username, so we don't skip them.
            if 'iglname' in user.keys():
                igl_player.igl_player_name = user['iglname']
            
            igl_player.discord_uid = user['id']
            igl_player.discord_username = user['username']
            igl_player.discord_avatar_url = user['avatar_url']

            if 'nick' in user.keys():
                igl_player.discord_nick = user['nick']
            
            igl_player.save()

            if update_player_avatars:

                # First try get player by player name
                player = Player.objects.filter(
                    name__iexact=igl_player.igl_player_name).first()
                
                # Attempt to get by discord username if player name doesn't work
                if not player:
                    player = Player.objects.filter(
                        discord_username__iexact=igl_player.discord_username).first()
                
                if player:
                    if not player.avatar_url:
                        player.avatar_url = igl_player.discord_avatar_url
                        player.save() 
                        print(f'Updating player avatar for {player.name}')

def parse_players_csv(csv_data):
    """
    Parse through CSV data of players, convert to a list of player data dicts.

    Arguments:
    csv_data -- Raw CSV data containing player information. (str)
    """
    rows = csv.reader(csv_data.splitlines(), delimiter=',')
    
    players = []
    headers = {
        'Player Name': None,
        'Phoentic': None,
        'Pronouns': None,
        'Primary In-game Name': None,
        'Secondary Alts': None,
        'Discord ID': None,
        'Twitch ID': None,
    }
    
    for idx, row in enumerate(rows):
        
        # Set Row Header Positions
        if idx == 0:
            continue

        if idx == 1:
            for key in headers.keys():
                headers[key] = row.index(key)        

        else:
            player = {}

            for key, val in headers.items():
                player[key.lower().replace(' ', '_')] = row[val]

            players.append(player)
    
    return players


def bulk_import_players(players):
    """
    Given a list of player data, bulk import into database.

    Since team import also brings in players, we are more cautious here as
    we don't want to disrupt those connections. Therefor, this import process
    only creates and updates existing player objects. 

    Arguments:
    players -- List of team data derived from team CSV sheet. (list)
    """
    pass
    player_count = {'created': 0, 'updated': 0}
    alias_count = {'created': 0, 'updated': 0, 'deleted': 0, 'skipped': 0}

    for entry in players:   
        
        # Skip bogus data
        if not entry['primary_in-game_name']:
            continue

        # Locate existing player object, ignoring case.
        player = Player.objects.filter(
            name__iexact=entry['player_name']).first()

        if player:
            player_count['updated'] += 1

        # Create (but don't commit) player object if not found 
        else:
            player = Player()
            player.name = entry['player_name']
            player_count['created'] += 1
                    
        player.name_phonetic =  entry['phoentic']
        player.pronouns = entry['pronouns']
        player.discord_username = entry['discord_id']
        player.twitch_username = entry['twitch_id']            
        player.save()  

        # Set primary in-game name
        primary_alias = player.aliases.filter(is_primary=True).first()

        if primary_alias:
            if primary_alias.name != entry['primary_in-game_name']:
                primary_alias.name = entry['primary_in-game_name']
                primary_alias.save()
                alias_count['updated'] += 1

        # If primary in game name field completed, set as main alias
        elif entry['primary_in-game_name']:
            try:
                Alias.objects.create(
                    player=player,
                    name=entry['primary_in-game_name'],
                    is_primary=True
                )
            
            # Trying to set more than one user's primary alias to the same
            # alias...possibly due to player rename
            except IntegrityError:
                pass

            alias_count['created'] += 1
        
        # If not, just use player name record as primary alias
        else:
            Alias.objects.create(
                player=player,
                name=player.name,
                is_primary=True
            )
            alias_count['created'] += 1
        
        # Set secondary alts
        secondary_aliases = entry['secondary_alts'].split(',')
        secondary_aliases = [x for x in secondary_aliases if x] # Weed out empty

        for alt in secondary_aliases:
            
            # Skip garbage entries
            if alt.lower() in ['none']:
                continue 
            
            alias = Alias.objects.filter(name__iexact=alt, player=player, is_primary=False).first()

            if alias:
                alias.name = alt
                alias.save()
                alias_count['updated'] += 1
            else:
                try:
                    Alias.objects.create(name=alt, player=player, is_primary=False)
                    alias_count['updated'] += 1
                except IntegrityError:
                    alias_count['skipped'] += 1

    return {'players': player_count, 'aliases': alias_count}
