from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from buzz.services import get_sheet_csv
from teams.services import parse_teams_csv, bulk_import_teams
from leagues.models import League, Season, Circuit
from matches.services import bulk_import_matches, parse_matches_csv

class Command(BaseCommand):
    help = 'Import all team and player data fresh from KQB Almanac'

    def add_arguments(self, parser):
        parser.add_argument('--league', type=str, help='Name of the league importing matches for')
        parser.add_argument('--season', type=str, help='Name of the season import matches for')

    def handle(self, *args, **options):
        league = League.objects.filter(name__icontains=options['league']).first()
        season = league.seasons.filter(name__icontains=options['season']).first()
        csv_data = get_sheet_csv(season.matches_csv_url)
        matches = parse_matches_csv(csv_data)

        result_count = bulk_import_matches(matches, season)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully imported {result_count["matches_created"]} Matches.')
        )

        if result_count['skipped']:
            self.stdout.write(self.style.NOTICE(
                    f'Skipped {result_count["skipped"]} rows.')
                )

