from django.contrib import admin
from django.conf import settings
from django.urls import path, re_path
from django.conf.urls import url, include
from django.conf.urls.static import static
import debug_toolbar
from .views import Home, DispatchAfterLogin, trigger_error

admin.site.site_header = 'Buzz Administration'

urlpatterns = [
    re_path(r'^api/', include('api.urls')),
    path('dispatch/', DispatchAfterLogin.as_view(), name='dispatch'),
    path('', Home.as_view(), name='home'),
    path('logging-debug/', trigger_error),
    re_path(r'^accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),        
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
