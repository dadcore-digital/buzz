from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from kqbapi.services import get_sheet_csv
from teams.services import parse_teams_csv, bulk_import_teams
from leagues.models import League, Season, Circuit

class Command(BaseCommand):
    help = 'Import all team and player data fresh from KQB Almanac'

    def handle(self, *args, **options):
        csv_data = get_sheet_csv(settings.TEAMS_CSV_URL)
        teams = parse_teams_csv(csv_data)
        league = League.objects.get(name='Indy Gaming League')
        season = Season.objects.get(league=league)
        circuit = Circuit.objects.first()
        result_count = bulk_import_teams(teams, league, season)

        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully imported {result_count["teams_created"]} Teams and {result_count["players_created"]} Players.')
        )