import csv
from django.db import IntegrityError
from buzz.services import get_sheet_csv
from leagues.models import Circuit
from players.models import Player
from .models import Team

def parse_teams_csv(csv_data):
    """
    Parse through CSV data of teams, convert to a list of team data dicts.

    Arguments:
    csv_data -- Raw CSV data containing team information. (str)
    """
    rows = csv.reader(csv_data.splitlines(), delimiter=',')
    
    teams = []
    headers = {
        'Tier': None,
        'Circuit': None,
        'Team': None,
        'Match Wins': None,
        'Matches Played': None,
        'Set Wins': None,
        'Captain': None,
        'all players': [],
        'Playoff Seed': None
    }
    
    for idx, row in enumerate(rows):
        
        # Set Row Header Positions
        if idx == 0:
            for key in headers.keys():
                headers[key] = row.index(key)        

        else:
            team = {}

            for key, val in headers.items():
                if key == 'all players':
                    team['members'] = row[12:19]  
                    
                    # Drop blank member entries
                    team['members'] = [x for x in team['members'] if x]
                else:
                    team[key.lower().replace(' ', '_')] = row[val]

            teams.append(team)

        # Calculate Extra Stats
        for team in teams:
            team['matches_lost'] = str(
                int(team['matches_played']) - int(team['match_wins']))
        
    return teams


def bulk_import_teams(teams, season, delete_before_import=False):
    """
    Given a list of team data, bulk import into database.

    Needs optimization in the future, but steps for now:

    1. Delete all existing teams.
    2. Loop through a dicictionary of teams.
    3. Create team based on data provided in teams list entries:        
        - Season and League provided by model instances passed into this 
          function.
        - Circuit FK assigned based on  values in 'circuit' and 'tier' keys
        - Player objects generated for all team members
            - Attempt to re-use a Player object if it already exists

    Arguments:
    team_list -- List of team data derived from team CSV sheet. (list)
    season -- A Season model instance to associate these teams with.
    delete_before_import -- Delete all existing Teams then initiate
                            import process. A way to start clean with
                            new data. (bool) (optional)
    """
    team_count = {'created': 0, 'updated': 0, 'deleted': 0}
    player_count = {'created': 0, 'updated': 0, 'deleted': 0}

    # Clear out all old data
    if delete_before_import:
        existing_teams = Team.objects.filter(circuit__in=season.circuits.all())
        team_count['deleted'] = existing_teams.count()
        existing_teams.delete()

    for entry in teams:
        # Basic team object
        circuit = season.circuits.filter(region=entry['circuit'], tier=entry['tier']).first()
        

        team, created = Team.objects.get_or_create(
            name__icontains=entry['team'], circuit=circuit)

        if created:        
            team_count['created'] += 1
            team.name = entry['team']
            team.save()
        else:
            team_count['updated'] += 1

        # Add members to team
        for member in entry['members']:
            player, created = Player.objects.get_or_create(name=member)

            if not team.members.filter(id=player.id).exists():
                team.members.add(player)

            
            if created:
                player_count['created'] += 1

        # Assign captain player object
        team.captain = Player.objects.filter(name=entry['captain']).first()
        team.save()
    
    return {'teams': team_count, 'players': player_count}
