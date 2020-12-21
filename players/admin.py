from django.contrib import admin
from django.utils.html import format_html
from .models import Player

class PlayerAdmin(admin.ModelAdmin):

    def member_of_teams(self):
        teams = ''


        for team in self.teams.all():
            teams += f'{team.name}, '
        
        teams = teams.strip().rstrip(',')
        return teams

    list_display = ('name', member_of_teams, 'discord_username', 'twitch_username')
    search_fields = ('name', 'teams__name')
    
    readonly_fields = (member_of_teams,)

admin.site.register(Player, PlayerAdmin)
