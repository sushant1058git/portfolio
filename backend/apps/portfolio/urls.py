from django.urls import path
from .views import (
    ProfileView, SkillsView, ExperienceView,
    EducationView, CertificationView, PortfolioSummaryView, ProjectListView, CurrentlyWorkingView
)
from .auth_views import LoginView, LogoutView, AuthCheckView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='api-profile'),
    path('skills/', SkillsView.as_view(), name='api-skills'),
    path('experience/', ExperienceView.as_view(), name='api-experience'),
    path('education/', EducationView.as_view(), name='api-education'),
    path('certifications/', CertificationView.as_view(), name='api-certifications'),
    path('summary/', PortfolioSummaryView.as_view(), name='api-summary'),

    path('auth/login/', LoginView.as_view(), name='api-login'),
    path('auth/logout/', LogoutView.as_view(), name='api-logout'),
    path('auth/check/', AuthCheckView.as_view(), name='api-auth-check'),
    path('projects/', ProjectListView.as_view(), name='api-projects'),
    path('currently-working/', CurrentlyWorkingView.as_view(), name='api-currently-working'),
]
