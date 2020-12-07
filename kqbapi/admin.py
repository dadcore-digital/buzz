import django.contrib.auth.admin
import django.contrib.auth.models
from django.contrib import admin, auth


admin.site.unregister(auth.models.Group)
