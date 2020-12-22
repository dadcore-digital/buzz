from django.contrib import admin
from django.utils.safestring import mark_safe
from buzz.services import get_object_admin_link
from .models import Player

class PlayerAdmin(admin.ModelAdmin):

    def member_of_teams(self):
        teams = ''


        for team in self.teams.all():
            team_link = get_object_admin_link(team, team.name)
            teams += f'{team_link}, '
        
        teams = teams.strip().rstrip(',')
        teams = mark_safe(teams)
        return teams

    def awards(self):
        awards = ''


        for award in self.awards.all():
            award_link = get_object_admin_link(award, award.award_category.name)
            awards += f'{award_link}, '
        
        awards = awards.strip().rstrip(',')
        awards = mark_safe(awards)
        return awards

    list_display = ('name', member_of_teams, 'discord_username', 'twitch_username')
    search_fields = ('name', 'teams__name')
    
    readonly_fields = (member_of_teams, awards)

admin.site.register(Player, PlayerAdmin)
