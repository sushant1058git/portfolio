from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Profile, SkillCategory, Experience, Education, Certification
from .serializers import (
    ProfileSerializer, SkillCategorySerializer, ExperienceSerializer,
    EducationSerializer, CertificationSerializer
)

from .models import Project, CurrentlyWorking, Scenario
from .models import Decision, FailureMode, ArchitectureDecisionRecord, Component, TrafficMetric, SimulatorBottleneck
from .serializers import ProjectSerializer, CurrentlyWorkingSerializer, ScenarioSerializer
from .serializers import (
    ScenarioDetailSerializer, DecisionSerializer, FailureModeSerializer,
    ArchitectureDecisionRecordSerializer, ComponentSerializer, TrafficMetricSerializer,
    SimulatorBottleneckSerializer,
)


class ProfileView(APIView):
    def get(self, request):
        try:
            profile = Profile.objects.first()
            if not profile:
                return Response({'error': 'Profile not found'}, status=404)
            serializer = ProfileSerializer(profile, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class SkillsView(APIView):
    def get(self, request):
        categories = SkillCategory.objects.prefetch_related('skills').all()
        serializer = SkillCategorySerializer(categories, many=True)
        return Response(serializer.data)


class ExperienceView(APIView):
    def get(self, request):
        experiences = Experience.objects.prefetch_related('points').all()
        serializer = ExperienceSerializer(experiences, many=True)
        return Response(serializer.data)


class EducationView(APIView):
    def get(self, request):
        education = Education.objects.all()
        serializer = EducationSerializer(education, many=True)
        return Response(serializer.data)


class CertificationView(APIView):
    def get(self, request):
        certs = Certification.objects.all()
        serializer = CertificationSerializer(certs, many=True)
        return Response(serializer.data)


class PortfolioSummaryView(APIView):
    """Single endpoint returning all portfolio data."""
    def get(self, request):
        profile = Profile.objects.first()
        skills = SkillCategory.objects.prefetch_related('skills').all()
        experiences = Experience.objects.prefetch_related('points').all()
        education = Education.objects.all()
        certs = Certification.objects.all()

        return Response({
            'profile': ProfileSerializer(profile, context={'request': request}).data if profile else None,
            'skills': SkillCategorySerializer(skills, many=True).data,
            'experience': ExperienceSerializer(experiences, many=True).data,
            'education': EducationSerializer(education, many=True).data,
            'certifications': CertificationSerializer(certs, many=True).data,
        })


class ProjectListView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        return Response(ProjectSerializer(projects, many=True, context={'request': request}).data)

class CurrentlyWorkingView(APIView):
    def get(self, request):
        items = CurrentlyWorking.objects.filter(is_active=True).order_by('-updated_at')
        return Response(CurrentlyWorkingSerializer(items, many=True).data)

class ScenarioListView(APIView):
    def get(self, request):
        scenarios = Scenario.objects.all()
        return Response(ScenarioSerializer(scenarios, many=True).data)


class ScenarioDetailView(APIView):
    """Full journey/decision/failure/ADR/simulator data for one scenario, fetched when it's opened."""
    def get(self, request, key):
        try:
            scenario = Scenario.objects.prefetch_related(
                'stages__points', 'stages__nodes', 'simulator_plans'
            ).get(key=key)
        except Scenario.DoesNotExist:
            return Response({'error': 'Scenario not found'}, status=404)
        return Response(ScenarioDetailSerializer(scenario).data)


class LabSharedView(APIView):
    """Content shared across every scenario: component-inspector info, traffic metrics, decisions,
    failure modes, ADRs, and simulator bottlenecks."""
    def get(self, request):
        components = Component.objects.all()
        return Response({
            'components': {c.name: ComponentSerializer(c).data for c in components},
            'traffic_metrics': TrafficMetricSerializer(TrafficMetric.objects.all(), many=True).data,
            'decisions': DecisionSerializer(Decision.objects.all(), many=True).data,
            'failure_modes': FailureModeSerializer(FailureMode.objects.all(), many=True).data,
            'adrs': ArchitectureDecisionRecordSerializer(ArchitectureDecisionRecord.objects.all(), many=True).data,
            'simulator_bottlenecks': SimulatorBottleneckSerializer(SimulatorBottleneck.objects.all(), many=True).data,
        })
