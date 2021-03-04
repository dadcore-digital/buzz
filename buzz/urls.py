from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from .views import Home, DispatchAfterLogin, trigger_error

admin.site.site_header = 'Buzz Administration'

urlpatterns = [
    url(r'^api/', include('api.urls')),
    path('dispatch/', DispatchAfterLogin.as_view(), name='dispatch'),
    path('', Home.as_view(), name='home'),
    path('logging-debug/', trigger_error),
    url(r'^accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    