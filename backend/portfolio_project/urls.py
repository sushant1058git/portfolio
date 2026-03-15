from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from apps.portfolio.status_views import StatusAPIView

admin.site.site_header = "Sushant Sinha · Portfolio Admin"
admin.site.site_title  = "Portfolio Admin"
admin.site.index_title = "Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),

    # API
    path('api/', include('apps.portfolio.urls')),
    path('api/', include('apps.blog.urls')),
    path('api/', include('apps.contact.urls')),

    # System status API
    path('api/status/', StatusAPIView.as_view(), name='api-status'),

    # Frontend pages
    path('',              TemplateView.as_view(template_name='index.html'),        name='home'),
    path('status/',       TemplateView.as_view(template_name='status.html'),       name='status'),
    path('blog/',         TemplateView.as_view(template_name='blog/list.html'),    name='blog-list'),
    path('blog/create/',  TemplateView.as_view(template_name='blog/editor.html'),  name='blog-editor'),
    path('blog/<slug:slug>/', TemplateView.as_view(template_name='blog/detail.html'), name='blog-detail'),
    path('contact/',      TemplateView.as_view(template_name='contact.html'),      name='contact'),
    path('playground/',   TemplateView.as_view(template_name='playground.html'),  name='playground'),
]

# Swagger / OpenAPI docs
try:
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularSwaggerView,
        SpectacularRedocView,
    )
    urlpatterns += [
        path('api/schema/',      SpectacularAPIView.as_view(),                             name='schema'),
        path('api/docs/',        SpectacularSwaggerView.as_view(url_name='schema'),        name='swagger-ui'),
        path('api/docs/redoc/',  SpectacularRedocView.as_view(url_name='schema'),          name='redoc'),
    ]
except ImportError:
    pass  # drf-spectacular not installed yet — routes simply won't exist

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)