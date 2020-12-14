from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from buzz.services import get_sheet_csv
from teams.services import parse_teams_csv, bulk_import_teams
from leagues.models import League, Season, Circuit

class Command(BaseCommand):
    help = 'Import all team and player data fresh from KQB Almanac'

    def add_arguments(self, parser):
        parser.add_argument('--league', type=str, help='Name of the league importing teams for')
        parser.add_argument('--season', type=str, help='Name of the season import teams for')
        parser.add_argument('--delete', action='store_true', help='Delete all teams and re-import from scratch')

    def handle(self, *args, **options):
        league = League.objects.filter(name__icontains=options['league']).first()
        season = league.seasons.filter(name__icontains=options['season']).first()
        csv_data = get_sheet_csv(season.teams_csv_url)
        teams = parse_teams_csv(csv_data)
        result_count = bulk_import_teams(
            teams, season, delete_before_import=options['delete'])

        
        self.stdout.write(self.style.SUCCESS(
            f'Created {result_count["teams"]["created"]} Teams and {result_count["players"]["created"]} Players.')
        )

        self.stdout.write(self.style.SUCCESS(
            f'Deleted {result_count["teams"]["deleted"]} Teams before importing.')
        )