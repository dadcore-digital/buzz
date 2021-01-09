import csv
from django.db import IntegrityError
from players.models import Player, Alias

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
            Alias.objects.create(
                player=player,
                name=entry['primary_in-game_name'],
                is_primary=True
            )
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
