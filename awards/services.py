import csv
from django.db import IntegrityError
from buzz.services import get_sheet_csv
from players.models import Player
from leagues.models import League, Season, Circuit, Round
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
        
        # Skip if only season data present, but no awards (placeholder rows)
        if not all([row[3], row[5], row[7], row[9], row[11]]):
            continue

        # Get Season Name and standardize
        season = row[0]
        if season.lower() == 'fall-20':
            season = 'Fall 2020'
        elif season.lower() == 'winter-21':
            season = 'Winter 2021'

        # Handle special weird week names like 'All'
        week = row[1]
        week_name = ''
        
        # Handle bye weeks
        if week.lower() == 'bye':
            week = 0.0
            week_name = 'Bye-Match'

        # Handle week 'all'
        elif week.lower() == 'bye':
            week = None
            week_name = 'All'

        # Other Non-Integer Weeks
        try:
            week = float(week)
        except ValueError:
            week = None
            week_name = week

        # Queen of the Hive
        if row[3] and row[4]:
            try:
                awards.append({
                'week': week,
                'week_name': week_name,
                'season': season,
                'tier': row[2][0],
                'region': row[2][1],
                'category': 'Queen of the Hive',
                'stats': [
                    {'category': 'KDR', 'total': float(row[3])},
                ],
                'player': row[4]
                })
            except ValueError:
                pass
        
        # Eternal Warrior
        if row[5] and row[6]:
            try:
                awards.append({
                'week': week,
                'week_name': week_name,
                'season': season,
                'tier': row[2][0],
                'region': row[2][1],
                'category': 'Eternal Warrior',
                'stats': [
                    {'category': 'Kills/Set', 'total': float(row[5])},
                ],
                'player': row[6]
                })
            except ValueError:
                pass

        # Purple Heart
        if row[7] and row[8]:
            try:
                awards.append({
                'week': week,
                'week_name': week_name,
                'season': season,
                'tier': row[2][0],
                'region': row[2][1],
                'category': 'Purple Heart',
                'stats': [
                    {'category': 'Deaths/Set & Win', 'total': float(row[7])},
                ],
                'player': row[8]
                })
            except ValueError:
                pass

        # Berry Bonanza	
        if row[9] and row[10]:
            try:
                awards.append({
                'week': week,
                'week_name': week_name,
                'season': season,
                'tier': row[2][0],
                'region': row[2][1],
                'category': 'Berry Bonanza',
                'stats': [
                    {'category': 'Berries/Set', 'total': float(row[9])},
                ],
                'player': row[10]
                })
            except ValueError:
                pass

        # Snail Whisperer
        if row[11] and row[12]:
            try:
                awards.append({
                'week': week,
                'week_name': week_name,
                'season': season,
                'tier': row[2][0],
                'region': row[2][1],
                'category': 'Snail Whisperer',
                'stats': [
                    {'category': 'Snail/Set', 'total': float(row[11])},
                ],
                'player': row[12]
                })
            except ValueError:
                pass

        # Triple Threat
        if all([row[13], row[14], row[15], row[16], row[17]]):
            try:
                awards.append({
                'week': week,
                'week_name': week_name,
                'season': season,
                'tier': row[2][0],
                'region': row[2][1],
                'category': 'Triple Threat',
                'stats': [
                    {'category': 'Score', 'total': float(row[13])},
                    {'category': 'Kills', 'total': float(row[15])},
                    {'category': 'Berries', 'total': float(row[16])},
                    {'category': 'Snail', 'total': float(row[17])},
                ],
                'player': row[14]
                }) 
            except ValueError:
                pass
    
    return awards


def bulk_import_awards(awards, delete_before_import=True):
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
    delete_before_import -- Delete all existing Awards then initiate
                            import process. A way to start clean with
                            new data. (bool) (optional)
    """
    award_count = {'created': 0, 'updated': 0, 'deleted': 0}
    player_count = {'created': 0, 'updated': 0, 'deleted': 0}
    
    # Clear out all old data
    if delete_before_import:
        existing_awards = Award.objects.all()
        award_count['deleted'] = existing_awards.count()
        existing_awards.delete()
    
    for entry in awards:
        
        category, category_created = AwardCategory.objects.get_or_create(
            name=entry['category'])

        player, player_created = Player.objects.get_or_create(
            name=entry['player'])
        
        league = League.objects.get(name='Indy Gaming League')
        season = Season.objects.get(name=entry['season'], league=league)

        circuit = Circuit.objects.filter(
            season=season, tier=entry['tier'], region=entry['region']).first()

        # Try getting round by number first, then by name

        round = season.rounds.filter(round_number=entry['week']).first()
        if not round:
            round = season.rounds.filter(name=entry['week_name']).first()

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
