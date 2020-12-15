import csv
from django.db import IntegrityError
from buzz.services import get_sheet_csv
from players.models import Player
from .models import Caster, NameMapping, Settings

def parse_casters_csv(csv_data):
    """
    Parse through CSV data of caster, convert to a list of caster data dicts.

    Arguments:
    csv_data -- Raw CSV data containing caster information. (str)
    """
    rows = csv.reader(csv_data.splitlines(), delimiter=',')
    ignore_names = Settings.objects.first().ignore_names.lower().split(',')
    casters = []
    headers = {
        'Community Caster': None,
        'Stream Link': None,
        'Bio': None,
    }

    for idx, row in enumerate(rows):
        
        # This sheet has a blank top row, skip it
        if idx == 0:
            continue
        # Set Row Header Positions
        elif idx == 1:
            for key in headers.keys():
                headers[key] = row.index(key)        

        else:
            caster = {}

            # Add caster row, unless in "ignore names" settings            
            if (
                row[1] and
                row[1].lower() not in ignore_names and
                len(row[1]) < 50
            ):
                for key, val in headers.items():
                    caster[key.lower().replace(' ', '_')] = row[val]

                casters.append(caster)
    
    return casters


def bulk_import_casters(caster_list, delete_before_import=True):
    """
    Given a list of caster data, bulk import into database.

    Needs optimization in the future, but steps for now:

    1. Delete all existing casters (if specified).
    2. Loop through a dicictionary of casters.
    3. Create Caster object based on data provided in Caster list entries:        
    4. Look for existing Player object to link to Caster
        - Create Player object and link to caster if does not exist

    Arguments:
    Caster_list -- List of caster data derived from team CSV sheet. (list)
    delete_before_import -- Delete all existing Caster then initiate
                            import process. A way to start clean with
                            new data. (bool) (optional)
    """
    caster_count = {'created': 0, 'updated': 0, 'deleted': 0}
    player_count = {'created': 0, 'updated': 0, 'deleted': 0}

    # Clear out all old data
    if delete_before_import:
        existing_casters = Caster.objects.all()
        caster_count['deleted'] = existing_casters.count()
        existing_casters.delete()
    
    for entry in caster_list:
        # Search for existing player and caster object
        player = Player.objects.filter(name=entry['community_caster']).first()
        player_created = False

        if not player:
            name_mapping = NameMapping.objects.filter(
                caster_name=entry['community_caster']).first()
            
            if name_mapping:
                player, player_created = Player.objects.get_or_create(
                    name=name_mapping.player_name)
            else:
                player, player_created = Player.objects.get_or_create(
                    name=entry['community_caster'])

        caster, caster_created = Caster.objects.get_or_create(player=player)
        caster.bio_link = entry['bio']
        caster.save()
        
        # Update Player Twitch Link
        twitch_username = entry['stream_link'].replace('twitch.tv/', '')
        player.twitch_username = twitch_username
        player.save()

        if player_created:
            player_count['created'] += 1
        
        if caster_created:
            caster_count['created'] += 1
    
    return {'casters': caster_count, 'players': player_count}
