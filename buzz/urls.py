from django.contrib import admin
from django.conf import settings
from django.urls import path, re_path
from django.conf.urls import url, include
from django.conf.urls.static import static
from .views import Home, DispatchAfterLogin, trigger_error

admin.site.site_header = 'Buzz Administration'

urlpatterns = [
    path('login/', Home.as_view(), name='home'),
    path('dispatch/', DispatchAfterLogin.as_view(), name='dispatch'),
    path('logging-debug/', trigger_error),
    re_path(r'^accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('admin/', include('loginas.urls')),
    path('staff/', include('staff.urls')),
    path('select2/', include("django_select2.urls")),
]

if settings.DEBUG_TOOLBAR:

    # Does not exist in CI
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),        
    ] 

if settings.DEBUG:
    
    urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [        

    # This MUST be last or it will break all other endpoints
    re_path(r'^', include('api.urls'))
]
