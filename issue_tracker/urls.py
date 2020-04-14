"""issue_tracker URL Configuration"""

from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import index


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^tickets/', include('tickets.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^checkout/', include('checkout.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
