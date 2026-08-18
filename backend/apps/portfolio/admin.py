from django.contrib import admin
from .models import Profile, SkillCategory, Skill, Experience, ExperiencePoint, Education, Certification


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'email', 'is_available', 'updated_at']
    fieldsets = (
        ('Basic Info', {'fields': ('name', 'role', 'tagline', 'bio', 'avatar', 'resume')}),
        ('Contact', {'fields': ('email', 'phone', 'github', 'linkedin', 'location')}),
        ('Stats', {'fields': ('years_experience', 'deploy_improvement', 'is_available')}),
    )


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'is_core', 'order']
    list_filter = ['is_core']
    inlines = [SkillInline]


class ExperiencePointInline(admin.TabularInline):
    model = ExperiencePoint
    extra = 2


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['role', 'company', 'start_date', 'is_current', 'order']
    list_filter = ['is_current']
    inlines = [ExperiencePointInline]


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'start_year', 'end_year', 'score']


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'issuer', 'year']


from .models import Project, CurrentlyWorking, Scenario
from .models import (
    Stage, StagePoint, StageNode, Component, Decision, FailureMode,
    ArchitectureDecisionRecord, TrafficMetric, SimulatorPlan, SimulatorBottleneck,
)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ['title', 'is_featured', 'order']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(CurrentlyWorking)
class CurrentlyWorkingAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'progress', 'is_active', 'updated_at']


class StageInline(admin.TabularInline):
    model = Stage
    extra = 0
    fields = ['key', 'mode', 'title', 'order']
    show_change_link = True


class SimulatorPlanInline(admin.TabularInline):
    model = SimulatorPlan
    extra = 0


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ['title', 'key', 'difficulty', 'order']
    prepopulated_fields = {'key': ('title',)}
    inlines = [StageInline, SimulatorPlanInline]


class StagePointInline(admin.TabularInline):
    model = StagePoint
    extra = 1


class StageNodeInline(admin.TabularInline):
    model = StageNode
    extra = 1


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ['scenario', 'key', 'mode', 'title', 'order']
    list_filter = ['scenario']
    inlines = [StagePointInline, StageNodeInline]


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'name']
    search_fields = ['name', 'display_name']


@admin.register(Decision)
class DecisionAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']


@admin.register(FailureMode)
class FailureModeAdmin(admin.ModelAdmin):
    list_display = ['name', 'impact', 'order']


@admin.register(ArchitectureDecisionRecord)
class ArchitectureDecisionRecordAdmin(admin.ModelAdmin):
    list_display = ['identifier', 'title', 'order']


@admin.register(TrafficMetric)
class TrafficMetricAdmin(admin.ModelAdmin):
    list_display = ['level', 'traffic_label', 'events', 'throughput', 'latency', 'error_rate']


@admin.register(SimulatorBottleneck)
class SimulatorBottleneckAdmin(admin.ModelAdmin):
    list_display = ['tier', 'text']