from django.contrib import admin
from django.utils.safestring import mark_safe
from buzz.services import get_object_admin_link
from .models import League, Season, Circuit, Group, Round
from teams.models import Team

class LeagueAdmin(admin.ModelAdmin):
    
    def seasons(self):
        links = ''
        for obj in self.seasons.all():
            link = get_object_admin_link(obj, obj)
            links += f'{link}, <br>'
        
        links = links[0:-6]
        links = mark_safe(links)
        return links
    
    readonly_fields = (seasons,)  

class SeasonAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'league',
        'is_active',
        'current_round',
        'registration_open',
        'rosters_open'        
    )   
 
    def circuits(self):
        links = ''
        for obj in self.circuits.all():
            link = get_object_admin_link(obj, obj)
            links += f'{link}, <br>'
        
        links = links[0:-6]
        links = mark_safe(links)
        return links
    
    def rounds(self):
        links = ''

        for obj in self.rounds.all():
            link = get_object_admin_link(obj, obj)
            links += f'{link}, <br>'
        
        links = links[0:-6]
        links = mark_safe(links)
        return links
    
    autocomplete_fields = ['current_round']
    readonly_fields = (circuits, rounds)  

class CircuitAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'region',
        'tier',
        'season'
    )   


    def teams(self):
        links = ''
        for obj in self.teams.all():
            link = get_object_admin_link(obj, obj)
            links += f'{link}, <br>'
        
        links = links[0:-6]
        links = mark_safe(links)
        return links
    
    
    search_fields = ('name',)
    readonly_fields = (teams,)  

class GroupAdmin(admin.ModelAdmin):
    
    list_display = (
        'circuit',
        'name',
        'number',
    )   

    def teams(self):
        links = ''
        for obj in self.teams.all():
            link = get_object_admin_link(obj, obj)
            links += f'{link}, <br>'
        
        links = links[0:-6]
        links = mark_safe(links)
        return links
    
    
    search_fields = ('name', 'circuit__name')
    readonly_fields = (teams,)  

class RoundAdmin(admin.ModelAdmin):
    
    list_display = (
        'season',
        'round_number',
        'name',
    )   

    search_fields = ('season__name',)


admin.site.register(League, LeagueAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Circuit, CircuitAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Round, RoundAdmin)
