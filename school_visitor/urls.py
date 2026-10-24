from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import never_cache


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('visitor.urls')),

    # PWA — serve manifest and service worker at root
    path('manifest.json', never_cache(TemplateView.as_view(
        template_name='manifest.json',
        content_type='application/manifest+json',
    )), name='manifest'),

    path('sw.js', never_cache(TemplateView.as_view(
        template_name='sw.js',
        content_type='application/javascript',
    )), name='serviceworker'),

    path('offline/', TemplateView.as_view(template_name='offline.html'), name='offline'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)