from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Profile, SkillCategory, Experience, Education, Certification
from .serializers import (
    ProfileSerializer, SkillCategorySerializer, ExperienceSerializer,
    EducationSerializer, CertificationSerializer
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
