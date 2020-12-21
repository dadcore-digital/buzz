from django.contrib import admin
from .models import Match, Result, Set, Game

class MatchAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'home', 'away', 'round', 'start_time', 'primary_caster')
    
    search_fields = (
        'home__name',
        'away__name',
        'circuit__name',
        'circuit__season__name',
        'primary_caster__player__name'
    )


admin.site.register(Match, MatchAdmin)
admin.site.register(Result)
admin.site.register(Set)
admin.site.register(Game)
