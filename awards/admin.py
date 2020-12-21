from django.contrib import admin
from .models import Award, AwardCategory, Stat, StatCategory

class AwardAdmin(admin.ModelAdmin):
    
    readonly_fields = ('stats',)

    list_display = (
        'award_category',
        'player',
        'circuit',
        'round',
    )   

    search_fields = ('award_category__name', 'player__name')

admin.site.register(Award, AwardAdmin)
admin.site.register(AwardCategory)
admin.site.register(Stat)
admin.site.register(StatCategory)



