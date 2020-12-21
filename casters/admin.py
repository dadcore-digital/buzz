from django.contrib import admin
from .models import Caster, NameMapping, Settings

class CasterAdmin(admin.ModelAdmin):
    
    list_display = (
        'player', 'bio_link', 'is_active', 'does_solo_casts'
    )

    search_fields = (
        'player__name',
    )



admin.site.register(Caster, CasterAdmin)
admin.site.register(NameMapping)
admin.site.register(Settings)
