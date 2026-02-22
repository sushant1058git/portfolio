from rest_framework import serializers
from .models import Profile, SkillCategory, Skill, Experience, ExperiencePoint, Education, Certification
from .models import Project, CurrentlyWorking


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
    avatar_url = serializers.SerializerMethodField()
    resume_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id', 'name', 'role', 'tagline', 'bio', 'email', 'phone',
            'github', 'linkedin', 'location', 'years_experience',
            'deploy_improvement', 'is_available',
            'avatar_url', 'resume_url',
        ]

    def get_avatar_url(self, obj):
        request = self.context.get('request')
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar.url)
        return None

    def get_resume_url(self, obj):
        request = self.context.get('request')
        if obj.resume and request:
            return request.build_absolute_uri(obj.resume.url)
        return None



class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'description', 'problem', 'outcome',
            'demo_url', 'github_url', 'cover_image', 'tech_stack',
            'github_stars', 'is_featured', 'order'
        ]

class CurrentlyWorkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentlyWorking
        fields = ['title', 'description', 'type', 'tech_tags', 'link', 'progress', 'updated_at']