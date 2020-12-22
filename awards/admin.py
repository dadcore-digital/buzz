from django.contrib import admin
from django.utils.safestring import mark_safe
from buzz.services import get_object_admin_link
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


class StatAdmin(admin.ModelAdmin):

    def player(self):
        award = self.award.all().first()
        if award:
            return self.award.all().first().player.name
        return ''

    def award_display(self):
        award = self.award.all().first()
        if award:
            return self.award.all().first()
        return ''

    list_display = (
        'stat_category',
        'total',
        player,
        award_display
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



