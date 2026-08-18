from rest_framework import serializers
from .models import Profile, SkillCategory, Skill, Experience, ExperiencePoint, Education, Certification
from .models import Project, CurrentlyWorking, Scenario
from .models import (
    Stage, StagePoint, StageNode, Component, Decision, FailureMode,
    ArchitectureDecisionRecord, TrafficMetric, SimulatorPlan, SimulatorBottleneck,
)


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'order']


class SkillCategorySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = SkillCategory
        fields = ['id', 'name', 'icon', 'is_core', 'skills']


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


class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = ['key', 'number', 'difficulty', 'title', 'description', 'requirement_chips']


class StageSerializer(serializers.ModelSerializer):
    points = serializers.SerializerMethodField()
    nodes = serializers.SerializerMethodField()

    class Meta:
        model = Stage
        fields = ['key', 'mode', 'title', 'text', 'points', 'nodes']

    def get_points(self, obj):
        return [p.text for p in obj.points.all()]

    def get_nodes(self, obj):
        return [n.name for n in obj.nodes.all()]


class DecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Decision
        fields = ['title', 'problem', 'decision', 'detail', 'alternatives']


class FailureModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FailureMode
        fields = ['name', 'impact', 'response', 'recovery']


class ArchitectureDecisionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchitectureDecisionRecord
        fields = ['identifier', 'title', 'detail']


class SimulatorPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulatorPlan
        fields = ['tier', 'name', 'diagram']


class ScenarioDetailSerializer(serializers.ModelSerializer):
    stages = serializers.SerializerMethodField()
    simulator_plans = serializers.SerializerMethodField()

    class Meta:
        model = Scenario
        fields = ['key', 'title', 'journey_title', 'stages', 'simulator_plans']

    def get_stages(self, obj):
        return {s.key: StageSerializer(s).data for s in obj.stages.all()}

    def get_simulator_plans(self, obj):
        return {p.tier: SimulatorPlanSerializer(p).data for p in obj.simulator_plans.all()}


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ['name', 'display_name', 'problem', 'decision', 'tradeoff', 'alternatives']


class TrafficMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficMetric
        fields = ['level', 'traffic_label', 'events', 'throughput', 'latency', 'error_rate', 'queue_lag', 'db_load']


class SimulatorBottleneckSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulatorBottleneck
        fields = ['tier', 'text']