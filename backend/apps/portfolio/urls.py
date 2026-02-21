from django.urls import path
from .views import (
    ProfileView, SkillsView, ExperienceView,
    EducationView, CertificationView, PortfolioSummaryView
)

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='api-profile'),
    path('skills/', SkillsView.as_view(), name='api-skills'),
    path('experience/', ExperienceView.as_view(), name='api-experience'),
    path('education/', EducationView.as_view(), name='api-education'),
    path('certifications/', CertificationView.as_view(), name='api-certifications'),
    path('summary/', PortfolioSummaryView.as_view(), name='api-summary'),
]
