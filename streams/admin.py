from django.contrib import admin
from .models import Stream, StreamerBlacklist

class StreamAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'username', 'start_time', 'service', 'is_live')
    search_fields = ('name', 'username', 'service')
    
class StreamerBlacklistAdmin(admin.ModelAdmin):
    
    list_display = ('username', 'reason')
    search_fields = ('username', 'reason')
    

admin.site.register(Stream, StreamAdmin)
admin.site.register(StreamerBlacklist, StreamerBlacklistAdmin)
