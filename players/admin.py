from django.contrib import admin
from django.utils.safestring import mark_safe
from buzz.services import get_object_admin_link
from .models import Alias, Player, PlayerSettings, IGLPlayerLookup

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

    def caster(self):
        caster_link = ''

        if hasattr(self, 'caster_profile'):
            caster_link = get_object_admin_link(self.caster_profile, self.caster_profile.id)
        
        caster_link = mark_safe(caster_link)
        return caster_link

    def casted_matches(self):
        matches = ''

        if hasattr(self, 'caster_profile'):

            for match in self.caster_profile.casted_matches.all():
                match_link = get_object_admin_link(match, f'{match.away.name} @ {match.home.name}')
                matches += f'{match_link}, '
        
        matches = matches.strip().rstrip(',')
        matches = mark_safe(matches)
        return matches

    def cocasted_matches(self):
        matches = ''

        if hasattr(self, 'caster_profile'):

            for match in self.caster_profile.cocasted_matches.all():
                match_link = get_object_admin_link(match, f'{match.away.name} @ {match.home.name}')
                matches += f'{match_link}, '
        
        matches = matches.strip().rstrip(',')
        matches = mark_safe(matches)
        return matches

    list_display = ('name', member_of_teams, 'discord_username', 'twitch_username')
    search_fields = ('name', 'teams__name')
    
    autocomplete_fields = ['user']

    readonly_fields = (
        member_of_teams, awards, caster, casted_matches, cocasted_matches)

class AliasAdmin(admin.ModelAdmin):

    list_display = ('player', 'name', 'is_primary')
    search_fields = ('name', 'player__name')

    autocomplete_fields = ['player']

class IGLPlayerLookupAdmin(admin.ModelAdmin):
    
    list_display = ('igl_player_name', 'discord_username', 'discord_uid', 'discord_nick', 'discord_avatar_url')
    search_fields = ('igl_player_name', 'discord_username', 'discord_uid')

admin.site.register(Player, PlayerAdmin)
admin.site.register(Alias, AliasAdmin)
admin.site.register(PlayerSettings)
admin.site.register(IGLPlayerLookup, IGLPlayerLookupAdmin)