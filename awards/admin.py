from django.contrib import admin
from django.utils.safestring import mark_safe
from buzz.services import get_object_admin_link
from .models import Award, AwardCategory, Stat, StatCategory

class AwardAdmin(admin.ModelAdmin):
    
    raw_id_fields = ('stats',)
    save_as = True
    
    list_display = (
        'award_category',
        'player',
        'circuit',
        'round',
    )   

    search_fields = (
        'award_category__name', 'player__name', 'circuit__season__name',
        'round__name'
    )

    autocomplete_fields = ['player']
    
class StatAdmin(admin.ModelAdmin):

    def player(self):
        award = self.award.first()
        if award:
            return award.player.name
        return ''

    def category(self):
        return self.stat_category.name

    list_display = (        
        'id',
        player,
        category,
        'total',
        
    )   


    def award(self):
        award_link = ''
        
        obj = self.award.first()

        if obj:
            award_link = get_object_admin_link(obj, obj)
            award_link = mark_safe(award_link)

        return award_link

    readonly_fields = (award,)

admin.site.register(Award, AwardAdmin)
admin.site.register(AwardCategory)
admin.site.register(Stat, StatAdmin)
admin.site.register(StatCategory)



