import csv
import time
from datetime import datetime, timedelta
from buzz.services import convert_et_to_utc
from leagues.models import League, Season, Circuit
from teams.models import Team
from .models import Match

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
        'Concatenate': None 
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

def bulk_import_matches(matches, league, season):
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

    Arguments:
    matches -- List of match dicts derived from matches CSV sheet. (list)
    league -- A League model instance to associate these teams with. (obj)
    season -- A Season model instance to associate these teams with. (obj)
    """
    # Clear out all old data
    Match.objects.all().delete()
    matches_created = 0

    for entry in matches:
        # Skip any matches that don't have a date
        match_date = entry['date']
        if ('TBD' in match_date
            or not match_date):
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

            Match.objects.create(
                home=home_team, away=away_team, circuit=circuit,
                start_time=utc_match_start
            )            

            matches_created += 1
    
    return {'matches_created': matches_created}
