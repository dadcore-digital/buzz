from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from buzz.services import get_sheet_csv
from players.services import bulk_import_players, parse_players_csv
from players.models import PlayerSettings

class Command(BaseCommand):
    help = 'Import/update all player data fresh from KQB Almanac'

    def handle(self, *args, **options):
        settings = PlayerSettings.objects.all().first()

        if settings:        
            csv_data = get_sheet_csv(settings.players_csv_url)
            players = parse_players_csv(csv_data)
            result_count = bulk_import_players(players)
        
            self.stdout.write(self.style.SUCCESS(
                f'Created {result_count["players"]["created"]} Players.')
            )
            self.stdout.write(self.style.SUCCESS(
                f'Updated {result_count["players"]["updated"]} Players.')
            )
            self.stdout.write(self.style.SUCCESS(
                f'Created {result_count["aliases"]["created"]} Aliases.')
            )

            self.stdout.write(self.style.SUCCESS(
                f'Skipped {result_count["aliases"]["skipped"]} Aliases.')
            )

        else:

            self.stdout.write(self.style.NOTICE(
                f'No Player Settings object found. Update aborted.')
            )


