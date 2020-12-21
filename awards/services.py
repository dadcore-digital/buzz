import csv
from django.db import IntegrityError
from buzz.services import get_sheet_csv
from players.models import Player
from leagues.models import Circuit, Round
from .models import Award, AwardCategory, Stat, StatCategory


def parse_awards_csv(csv_data):
    """
    Parse through CSV data of awards, convert to a list of award data dicts.

    Arguments:
    csv_data -- Raw CSV data containing awards information. (str)
    """
    rows = csv.reader(csv_data.splitlines(), delimiter=',')
    awards = []

    for idx, row in enumerate(rows):
        # Skip header rows
        if idx < 2 or not all([row[0], row[1]]):
            continue
        
        # Handle special weird week names
        week = row[0]
        if 'bye' in week.lower():
            week = 9999

        # Queen of the Hive
        if row[2] and row[3]:
            try:
                awards.append({
                'week': week,
                'tier': row[1][0],
                'region': row[1][1],
                'category': 'Queen of the Hive',
                'stats': [
                    {'category': 'KDR', 'total': float(row[2])},
                ],
                'player': row[3]
                })
            except ValueError:
                pass

        # Eternal Warrior
        if row[4] and row[5]:
            try:
                awards.append({
                'week': week,
                'tier': row[1][0],
                'region': row[1][1],
                'category': 'Eternal Warrior',
                'stats': [
                    {'category': 'Kills/Set', 'total': float(row[4])},
                ],
                'player': row[5]
                })
            except ValueError:
                pass

        # Purple Heart
        if row[6] and row[7]:
            try:
                awards.append({
                'week': week,
                'tier': row[1][0],
                'region': row[1][1],
                'category': 'Purple Heart',
                'stats': [
                    {'category': 'Deaths/Set & Win', 'total': float(row[6])},
                ],
                'player': row[7]
                })
            except ValueError:
                pass

        # Berry Bonanza	
        if row[8] and row[9]:
            try:
                awards.append({
                'week': week,
                'tier': row[1][0],
                'region': row[1][1],
                'category': 'Berry Bonanza',
                'stats': [
                    {'category': 'Berries/Set', 'total': float(row[8])},
                ],
                'player': row[9]
                })
            except ValueError:
                pass

        # Snail Whisperer
        if row[10] and row[11]:
            try:
                awards.append({
                'week': week,
                'tier': row[1][0],
                'region': row[1][1],
                'category': 'Snail Whisperer',
                'stats': [
                    {'category': 'Snail/Set', 'total': float(row[10])},
                ],
                'player': row[11]
                })
            except ValueError:
                pass

        # Triple Threat
        if all([row[12], row[14], row[15], row[16]]):
            try:
                awards.append({
                'week': week,
                'tier': row[1][0],
                'region': row[1][1],
                'category': 'Triple Threat',
                'stats': [
                    {'category': 'Score', 'total': float(row[12])},
                    {'category': 'Kills', 'total': float(row[14])},
                    {'category': 'Berries', 'total': float(row[15])},
                    {'category': 'Snail', 'total': float(row[16])},
                ],
                'player': row[13]
                }) 
            except ValueError:
                pass
    
    return awards


def bulk_import_awards(awards, season, delete_before_import=True):
    """
    Given a list of caster data, bulk import into database.

    Needs optimization in the future, but steps for now:

    1. Delete all existing awards (if specified).
    2. Loop through a dicictionary of awards.
    3. Create Award and Stat objects based on data provided in the award
       list entry.
    4. Look for existing Player object to link to Award
        - Create Player object and link to Award if does not exist

    Arguments:
    awards -- List of awards data derived from team CSV sheet. (list)
    season -- A Season model instance to associate these awards with.
    delete_before_import -- Delete all existing Awards then initiate
                            import process. A way to start clean with
                            new data. (bool) (optional)
    """
    award_count = {'created': 0, 'updated': 0, 'deleted': 0}
    player_count = {'created': 0, 'updated': 0, 'deleted': 0}
    
    # Clear out all old data
    if delete_before_import:
        existing_awards = Award.objects.filter(circuit__season=season)        
        award_count['deleted'] = existing_awards.count()
        existing_awards.delete()
    
    for entry in awards:
        
        category, category_created = AwardCategory.objects.get_or_create(
            name=entry['category'])

        player, player_created = Player.objects.get_or_create(
            name=entry['player'])
        
        circuit = Circuit.objects.filter(
            season=season, tier=entry['tier'], region=entry['region']).first()

        round = season.rounds.filter(round_number=entry['week']).first()

        award, award_created = Award.objects.get_or_create(
            award_category=category, circuit=circuit, round=round, player=player
        )  
        
        for record in entry['stats']:
            stat_category, stat_cat_created = StatCategory.objects.get_or_create(
                name=record['category']
            )
            stat = award.stats.filter(stat_category=stat_category).first()
            if not stat:
                stat = Stat(stat_category=stat_category)
            stat.total = record['total']
            stat.save()
            award.stats.add(stat)
        
        if award_created:
            award_count['created'] += 1

        if player_created:
            player_count['created'] += 1
            
    return {'awards': award_count, 'players': player_count}
