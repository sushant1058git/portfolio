from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Customize admin
admin.site.site_header = "Sushant Sinha · Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include('apps.portfolio.urls')),
    path('api/', include('apps.blog.urls')),
    path('api/', include('apps.contact.urls')),

    # Frontend — serve index.html for all non-API routes (SPA style)
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('blog/', TemplateView.as_view(template_name='blog/list.html'), name='blog-list'),
    path('blog/create/', TemplateView.as_view(template_name='blog/editor.html'), name='blog-editor'),
    path('blog/<slug:slug>/', TemplateView.as_view(template_name='blog/detail.html'), name='blog-detail'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
