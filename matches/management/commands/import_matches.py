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
        parser.add_argument('--delete', action='store_true', help='Delete all matches and re-import from scratch')

    def handle(self, *args, **options):
        league = League.objects.filter(name__icontains=options['league']).first()
        season = league.seasons.filter(name__icontains=options['season']).first()
        csv_data = get_sheet_csv(season.matches_csv_url)
        matches = parse_matches_csv(csv_data)

        result_count = bulk_import_matches(
            matches, season, delete_before_import=True)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully imported {result_count["matches"]["created"]} Matches.')
        )

        self.stdout.write(self.style.SUCCESS(
            f'Deleted {result_count["matches"]["deleted"]} Matches before importing.')
        )

        if result_count['matches']['skipped']:
            self.stdout.write(self.style.NOTICE(
                    f'Skipped {result_count["matches"]["skipped"]} rows.')
                )


