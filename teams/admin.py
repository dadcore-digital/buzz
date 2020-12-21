from django.contrib import admin
from .models import Team

class TeamAdmin(admin.ModelAdmin):
    
    def members(self):
        members = ''

        for member in self.members.all():
            members += f'{member.name}, '
        
        members = members.strip().rstrip(',')
        return members

    list_display = ('name', 'captain', members, 'circuit')
    search_fields = ('name', 'members__name')
    
admin.site.register(Team, TeamAdmin)
