from django.contrib import admin
from .models import League, Season, Circuit, Bracket, Round

admin.site.register(League)
admin.site.register(Season)
admin.site.register(Circuit)
admin.site.register(Bracket)
admin.site.register(Round)
