from rest_framework import serializers
from .models import Profile, SkillCategory, Skill, Experience, ExperiencePoint, Education, Certification


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'order']


class SkillCategorySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = SkillCategory
        fields = ['id', 'name', 'icon', 'skills']


class ExperiencePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperiencePoint
        fields = ['id', 'text', 'order']


class ExperienceSerializer(serializers.ModelSerializer):
    points = ExperiencePointSerializer(many=True, read_only=True)
    period = serializers.ReadOnlyField()

    class Meta:
        model = Experience
        fields = ['id', 'role', 'company', 'location', 'period', 'is_current', 'points', 'order']


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id', 'name', 'role', 'tagline', 'bio', 'email', 'phone',
            'github', 'linkedin', 'location', 'years_experience',
            'deploy_improvement', 'avatar', 'is_available'
        ]
