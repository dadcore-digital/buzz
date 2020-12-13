from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from buzz.services import get_sheet_csv
from teams.services import parse_teams_csv, bulk_import_teams
from leagues.models import League, Season, Circuit
from matches.services import bulk_import_matches, parse_matches_csv

class Command(BaseCommand):
    help = 'Import all team and player data fresh from KQB Almanac'

    def handle(self, *args, **options):
        csv_data = get_sheet_csv(settings.MATCHES_CSV_URL)
        matches = parse_matches_csv(csv_data)
        league = League.objects.get(name='Indy Gaming League')
        season = Season.objects.get(league=league)
        result_count = bulk_import_matches(matches, league, season)


        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully imported {result_count["matches_created"]} Matches.')
        )
