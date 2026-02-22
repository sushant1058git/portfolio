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
    list_display = ['name', 'icon', 'order']
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


from .models import Project, CurrentlyWorking

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ['title', 'is_featured', 'order']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(CurrentlyWorking)
class CurrentlyWorkingAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'progress', 'is_active', 'updated_at']