from django.contrib import admin
from django.utils.safestring import mark_safe
from buzz.services import get_object_admin_link
from .models import Caster, NameMapping, Settings

class CasterAdmin(admin.ModelAdmin):
    
    list_display = (
        'player', 'bio_link', 'is_active', 'does_solo_casts'
    )

    search_fields = (
        'player__name',
    )

    def casted_matches(self):
        matches = ''

        for match in self.casted_matches.all():
            match_link = get_object_admin_link(match, f'{match.away.name} @ {match.home.name}')
            matches += f'{match_link}, '
        
        matches = matches.strip().rstrip(',')
        matches = mark_safe(matches)
        return matches

    def cocasted_matches(self):
        matches = ''

        for match in self.cocasted_matches.all():
            match_link = get_object_admin_link(match, f'{match.away.name} @ {match.home.name}')
            matches += f'{match_link}, '
        
        matches = matches.strip().rstrip(',')
        matches = mark_safe(matches)
        return matches

    autocomplete_fields = ['player', 'alias']
    readonly_fields = (casted_matches, cocasted_matches)


admin.site.register(Caster, CasterAdmin)
admin.site.register(NameMapping)
admin.site.register(Settings)
