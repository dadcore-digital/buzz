from django.core.management.base import BaseCommand, CommandError
from streams.services import update_twitch_streams

class Command(BaseCommand):
    help = 'Update listing of current streams for KQB.'

    def handle(self, *args, **options):
        results = update_twitch_streams()
        self.stdout.write(
            self.style.SUCCESS(f'Created Streams {results["created"]}'))

        self.stdout.write(
            self.style.SUCCESS(f'Updated Streams {results["updated"]}'))

        self.stdout.write(
            self.style.SUCCESS(f'Total Live Streams {results["total"]}'))
