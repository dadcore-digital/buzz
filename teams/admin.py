from django.contrib import admin
from django.utils.safestring import mark_safe
from buzz.services import get_object_admin_link
from .models import Dynasty, Team
    
class TeamAdmin(admin.ModelAdmin):
    
    def members(self):
        members = ''

        for member in self.members.all():
            members += f'{member.name}, '
        
        members = members.strip().rstrip(',')
        return members

    list_display = ('name', 'dynasty', 'captain', members, 'circuit')
    search_fields = ('name', 'dynasty__name', 'members__name')
    
    autocomplete_fields = ['members', 'dynasty']


class TeamInline(admin.StackedInline):
    model = Team

class DynastyAdmin(admin.ModelAdmin):
    
    list_display = ('name',)
    search_fields = ('name',)

    def teams(self):
        links = ''

        for obj in self.teams.all():
            link = get_object_admin_link(obj, obj)
            links += f'{link}, <br>'
        
        links = links[0:-6]
        links = mark_safe(links)
        return links
    
    readonly_fields = (teams,)  


admin.site.register(Dynasty, DynastyAdmin)
admin.site.register(Team, TeamAdmin)

