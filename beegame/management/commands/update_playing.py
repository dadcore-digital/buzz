from django.core.management.base import BaseCommand, CommandError
from beegame.services import update_steam_playing_count

class Command(BaseCommand):
    help = 'Update count of people currently playing KQB.'

    def handle(self, *args, **options):
        playing_count_obj = update_steam_playing_count()
        self.stdout.write(self.style.SUCCESS(f'Created {playing_count_obj}'))
