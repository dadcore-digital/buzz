from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from buzz.services import get_sheet_csv
from awards.services import parse_awards_csv, bulk_import_awards
from leagues.models import League, Season, Circuit

class Command(BaseCommand):
    help = 'Import all team and player data fresh from KQB Almanac'

    def add_arguments(self, parser):
        parser.add_argument('--league', type=str, help='Name of the league importing awards for')
        parser.add_argument('--season', type=str, help='Name of the season importing awards for')
        parser.add_argument('--delete', action='store_true', help='Delete all awards and re-import from scratch')

    def handle(self, *args, **options):
        league = League.objects.filter(name__icontains=options['league']).first()
        season = league.seasons.filter(name__icontains=options['season']).first()
        csv_data = get_sheet_csv(season.awards_csv_url)
        awards = parse_awards_csv(csv_data)
        result_count = bulk_import_awards(
            awards, season, delete_before_import=options['delete'])

        
        self.stdout.write(self.style.SUCCESS(
            f'Created {result_count["awards"]["created"]} Awards and {result_count["players"]["created"]} Players.')
        )

        self.stdout.write(self.style.SUCCESS(
            f'Deleted {result_count["awards"]["deleted"]} Awards before importing.')
        )
