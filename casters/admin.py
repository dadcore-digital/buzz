from django.contrib import admin
from .models import Caster, NameMapping, Settings

admin.site.register(Caster)
admin.site.register(NameMapping)
admin.site.register(Settings)
