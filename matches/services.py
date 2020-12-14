import csv
import time
from datetime import datetime, timedelta
from django.db import IntegrityError
from buzz.services import convert_et_to_utc
from leagues.models import League, Season, Circuit
from teams.models import Team
from .models import Match, Result, Set

def parse_matches_csv(csv_data):
    """
    Parse through CSV data of matches, convert to a list of match data dicts.

    Arguments:
    csv_data -- Raw CSV data containing match information. (str)
    """
    rows = csv.reader(csv_data.splitlines(), delimiter=',')
    
    matches = []
    headers = {
        'Tier': None,
        'Circ': None,
        'Away Team': None,
        'Home Team': None,
        'Time (Eastern)': None,
        'Date': None,
        'Caster': None,
        'Co-casters': None,
        'Stream Link': None,
        'VOD Link': None,
        'Away Sets Won': None,
        'Home Sets Won': None,
        'Winner': None
    }

    for idx, row in enumerate(rows):
    
        # Set Row Header Positions
        if idx == 0:
            for key in headers.keys():
                headers[key] = row.index(key)        

        else:
            match = {}

            for key, val in headers.items():
                match[key.lower().replace(' ', '_')] = row[val]
            
            matches.append(match)

    return matches

def bulk_import_matches(matches, season, delete_before_import=True):
    """
    Given a list of match data, bulk import into database.

    Needs optimization in the future, but steps for now:

    1. Delete all existing matches
    2. Loop through a dict list of all matches
    3. Create match objects for each entry
        - Take 'tier' and 'circ' fields to match to existing Circuit object
        - Match team names in `home_team` and `away_team` to existing team
          objects in database.
        - Convert match time from ET to UTC
        - TODO: Match 'caster' to existing caster entry in database (text for 
                now)            
    4. Create Result object if Match has declared winner.

    Arguments:
    matches -- List of match dicts derived from matches CSV sheet. (list)
    season -- A Season model instance to associate these teams with. (obj)
    delete_before_import -- Delete all existing Matches then initiate
                            import process. A way to start clean with
                            new data. (bool) (optional)
    """
    # Clear out all old data
    match_count = {
        'created': 0,
        'deleted': 0,
        'skipped': 0
    }

    # Currently deleting before import as we don't have a unique way to
    # identify matches, so no way to update them in place. This functionality
    # is here for future use. 
    if delete_before_import:
        existing_matches = Match.objects.filter(circuit__season=season)
        match_count['deleted'] = existing_matches.count()
        existing_matches.delete()

    for entry in matches:
        # Skip any matches that don't have a date
        match_date = entry['date']
        if ('TBD' in match_date
            or not match_date):
            match_count['skipped'] += 1
            continue
        else:
            # Determine circuit, home team, and away team fields to existing
            # objects in database.
            circuit = season.circuits.filter(region=entry['circ'], tier=entry['tier']).first()
            home_team = Team.objects.filter(circuit=circuit, name=entry['home_team']).first()
            away_team = Team.objects.filter(circuit=circuit, name=entry['away_team']).first()
                
            # Set all invalid/TDB times to midnight
            match_time = entry['time_(eastern)']

            # We don't need seconds                            
            match_time = match_time.replace(':00:00', ':00')
            match_time = match_time.replace(':30:00', ':30')

            try:
                match_time = datetime.strptime(match_time, '%I:%M %p').strftime('%H:%M') 
            
            # Set invalid match times to midnight
            except ValueError:
                match_time = '00:00'

            # Convert match time from ET to UTC
            et_match_start = datetime.strptime(f'{match_date} {match_time}', '%Y-%m-%d %H:%M')
            utc_match_start = convert_et_to_utc(et_match_start)

            try:
                match = Match.objects.create(
                    home=home_team, away=away_team, circuit=circuit,
                    start_time=utc_match_start
                )            
                match_count['created'] += 1

                # Create Result and Set Objects if Winner defined
                if entry['winner']:
                    if entry['winner'] == match.home.name:
                        match_winner = match.home
                        match_loser = match.away
                    else:
                        match_winner = match.away
                        match_loser = match.home
                    
                    # Create Result object to record match details
                    result = Result.objects.create(
                        match=match, winner=match_winner, loser=match_loser)

                    # Create Set objects for game and assign winner and loser
                    home_sets_won = int(entry['home_sets_won'])
                    away_sets_won = int(entry['away_sets_won'])

                    # Sets for home team
                    for number in range(1, home_sets_won + 1):
                        Set.objects.create(
                            result=result,
                            number = number,
                            winner = match.home,
                            loser = match.away
                        )
                    
                    # Sets for away team
                    for number in range(1, away_sets_won + 1):
                        Set.objects.create(
                            result=result,
                            number = number,
                            winner = match.away,
                            loser = match.home
                        )
                    
            # Encountered some error/missing field
            except IntegrityError:
                match_count['skipped'] += 1
    
    return {'matches': match_count }
        