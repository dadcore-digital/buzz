from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from buzz.services import get_object_admin_link
from .models import Match, Result, Set, SetLog, Game, PlayerMapping, TeamMapping

class MatchAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'home', 'away', 'round', 'group', 'start_time', 'primary_caster', 'created', 'modified')
    
    search_fields = (
        'home__name',
        'away__name',
        'circuit__name',
        'circuit__season__name',
        'group__name',
        'primary_caster__player__name',
    )

    def result(self):
        result_link = ''
        
        if self.result:
            result_link = get_object_admin_link(self.result, self.result)
            result_link = mark_safe(result_link)

        return result_link

    readonly_fields = (result,)
    autocomplete_fields = [
        'home', 'away', 'circuit', 'round', 'primary_caster', 'secondary_casters'
    ]

class ResultAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'match',
        'status',
        'winner',
        'loser',
        'source',
        'created_by'
    ]

    search_fields = (
        'match__home__name',
        'match__away__name',
        'match__circuit__name',
        'match__circuit__season__name',
        'status'
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(
            ResultAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'notes':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield

    def sets(self):
        sets = ''

        for obj in self.sets.all():
            set_link = get_object_admin_link(obj, obj)
            sets += f'{set_link}, <br>'
        
        sets = sets[0:-6]
        sets = mark_safe(sets)
        return sets

    def player_mappings(self):
        player_mappings = ''

        for obj in self.player_mappings.all():
            mapping_link = get_object_admin_link(obj, obj)
            player_mappings += f'{mapping_link}, <br>'
        
        player_mappings = player_mappings[0:-6]
        player_mappings = mark_safe(player_mappings)
        return player_mappings

    def team_mappings(self):
        team_mappings = ''

        for obj in self.team_mappings.all():
            mapping_link = get_object_admin_link(obj, obj)
            team_mappings += f'{mapping_link}, <br>'
        
        team_mappings = team_mappings[0:-6]
        team_mappings = mark_safe(team_mappings)
        return team_mappings

    readonly_fields = (sets, player_mappings, team_mappings)    
    autocomplete_fields = ['match', 'winner', 'loser', 'created_by']


class SetAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'result',
        'number',
        'winner',
        'loser'
    ]
    
    def result(self):
        result_link = ''

        if self.result:
            result_link = get_object_admin_link(self.result, self.result)
            result_link = mark_safe(result_link)

        return result_link

    def games(self):
        games = ''

        for obj in self.games.all():
            game_link = get_object_admin_link(obj, obj)
            games += f'{game_link}, <br>'
        
        games = games[0:-6]
        games = mark_safe(games)
        return games

    def log(self):
        log_link = ''

        if self.log:
            log_link = get_object_admin_link(self.log, self.log)
            log_link = mark_safe(log_link)

        return log_link

    readonly_fields = (games, result, log)
    search_fields = [
        'match__home__name',
        'match__away__name'
    ]
    autocomplete_fields = ['result', 'winner', 'loser']

class SetLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'set', 'filename']
    autocomplete_fields = ['set']

class GameAdmin(admin.ModelAdmin):
    
    list_display = [
        'id', 'set', 'map', 'number', 'winner', 'loser', 'win_condition' 
    ]
    autocomplete_fields = ['winner', 'loser']
    raw_id_fields = ['set']

class PlayerMappingAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'nickname', 'player', 'result' )
    
    search_fields = (
        'id',
        'nickname',
        'result__match__home__name',
        'result__match__away__name',
        'player__name',
    )

    autocomplete_fields = [
        'result', 'player'
    ]

class TeamMappingAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'color', 'team', 'result' )
    
    search_fields = (
        'id',
        'color',
        'result__match__home__name',
        'result__match__away__name',
        'team__name',
    )

    autocomplete_fields = [
        'result', 'team'
    ]

admin.site.register(Match, MatchAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Set, SetAdmin)
admin.site.register(SetLog, SetLogAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(PlayerMapping, PlayerMappingAdmin)
admin.site.register(TeamMapping, TeamMappingAdmin)
