from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from apps.portfolio.status_views import StatusAPIView
from apps.portfolio.external_views import GitHubProfileView, LeetCodeProfileView
from apps.blog.views import blog_editor_view, access_denied_view

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

    # External coding-profile APIs
    path('api/github-profile/', GitHubProfileView.as_view(), name='api-github-profile'),
    path('api/leetcode-profile/', LeetCodeProfileView.as_view(), name='api-leetcode-profile'),

    # Frontend pages
    path('',              TemplateView.as_view(template_name='index.html'),        name='home'),
    path('status/',       TemplateView.as_view(template_name='status.html'),       name='status'),
    path('access-denied/', access_denied_view,                                     name='access-denied'),
    path('blog/',         TemplateView.as_view(template_name='blog/list.html'),    name='blog-list'),
    path('blog/create/',  blog_editor_view,                                        name='blog-editor'),
    path('blog/<slug:slug>/', TemplateView.as_view(template_name='blog/detail.html'), name='blog-detail'),
    path('contact/',      TemplateView.as_view(template_name='contact.html'),      name='contact'),
    path('playground/',   TemplateView.as_view(template_name='playground.html'),  name='playground'),
    path('labs/architecture/', TemplateView.as_view(template_name='architecture_lab.html'), name='architecture-lab'),
    path('labs/github/',  TemplateView.as_view(template_name='github_profile.html'), name='github-profile'),
    path('labs/leetcode/', TemplateView.as_view(template_name='leetcode_profile.html'), name='leetcode-profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
    # Serve the source static directory in development so newly added Lab assets
    # work immediately without requiring collectstatic or a container restart.
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
