from django.contrib import admin
from django.utils.safestring import mark_safe
from buzz.services import get_object_admin_link
from .models import Match, Result, Set, Game

class MatchAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'home', 'away', 'round', 'start_time', 'primary_caster', 'created', 'modified')
    
    search_fields = (
        'home__name',
        'away__name',
        'circuit__name',
        'circuit__season__name',
        'primary_caster__player__name'
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
    
    search_fields = (
        'match__home__name',
        'match__away__name',
        'match__circuit__name',
        'match__circuit__season__name',
        'status'
    )

    def sets(self):
        sets = ''

        for obj in self.sets.all():
            set_link = get_object_admin_link(obj, obj)
            sets += f'{set_link}, <br>'
        
        sets = sets[0:-6]
        sets = mark_safe(sets)
        return sets
    
    readonly_fields = (sets,)    

class SetAdmin(admin.ModelAdmin):
    
    def result(self):
        result_link = ''

        if self.result:
            result_link = get_object_admin_link(self.result, self.result)
            result_link = mark_safe(result_link)

        return result_link

    readonly_fields = (result,)


admin.site.register(Match, MatchAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Set, SetAdmin)
admin.site.register(Game)
