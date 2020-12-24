from django.contrib import admin
from .models import Playing, Release

class PlayingAdmin(admin.ModelAdmin):
    
    list_display = ('total', 'updated', 'platform')
    search_fields = ('total', 'updated')
    
class ReleaseAdmin(admin.ModelAdmin):
    
    list_display = ('buildid', 'version', 'title', 'released_on')
    search_fields = ('builid', 'version', 'title')
    

admin.site.register(Playing, PlayingAdmin)
admin.site.register(Release, ReleaseAdmin)
