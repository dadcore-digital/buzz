from django.contrib import admin
from django.utils.safestring import mark_safe
from buzz.services import get_object_admin_link
from .models import League, Season, Circuit, Bracket, Round


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
    
    readonly_fields = (circuits, rounds)  

class CircuitAdmin(admin.ModelAdmin):
    
    def teams(self):
        links = ''
        for obj in self.teams.all():
            link = get_object_admin_link(obj, obj)
            links += f'{link}, <br>'
        
        links = links[0:-6]
        links = mark_safe(links)
        return links
    
    readonly_fields = (teams,)  

admin.site.register(League, LeagueAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Circuit, CircuitAdmin)
admin.site.register(Bracket)
admin.site.register(Round)
