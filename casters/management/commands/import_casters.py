from django.core.management.base import BaseCommand, CommandError
from buzz.services import get_sheet_csv
from casters.services import parse_casters_csv, bulk_import_casters
from casters.models import Caster, Settings

class Command(BaseCommand):
    help = 'Import all team and player data fresh from KQB Almanac'

    def add_arguments(self, parser):
        parser.add_argument('--delete', action='store_true', help='Delete all casters and re-import from scratch')

    def handle(self, *args, **options):
        settings = Settings.objects.first()
        csv_data = get_sheet_csv(settings.casters_csv_url)
        casters = parse_casters_csv(csv_data)

        result_count = bulk_import_casters(casters, delete_before_import=options['delete'])

        self.stdout.write(self.style.SUCCESS(
            f'Created {result_count["casters"]["created"]} Casters and {result_count["players"]["created"]} Players.')
        )

        self.stdout.write(self.style.SUCCESS(
            f'Deleted {result_count["casters"]["deleted"]} Casters before importing.')
        )
