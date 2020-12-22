from django.contrib import admin
from .models import Event, EventLink

class EventLinkInline(admin.TabularInline):
    model = EventLink

class EventAdmin(admin.ModelAdmin):
    
    def organizers(self):
        organizers = ''

        for organizer in self.organizers.all():
            organizers += f'{organizer.name}, '
        
        organizers = organizers.strip().rstrip(',')
        return organizers

    list_display = ('name', 'start_time', organizers, 'created')
    search_fields = ('name',)
    
    autocomplete_fields = ['organizers']

    inlines = (EventLinkInline,)

class EventLinkAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'url', 'event')
    search_fields = ('name', 'event__name')
    

admin.site.register(Event, EventAdmin)
admin.site.register(EventLink, EventLinkAdmin)
