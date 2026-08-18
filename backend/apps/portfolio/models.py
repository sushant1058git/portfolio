from django.db import models


class Profile(models.Model):
    """Sushant's profile info — only one instance needed."""
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300, blank=True)
    bio = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    location = models.CharField(max_length=100, default='Bangalore, India')
    years_experience = models.PositiveIntegerField(default=5)
    deploy_improvement = models.CharField(max_length=20, default='30%')
    avatar = models.ImageField(upload_to='profile/', blank=True, null=True)
    resume = models.FileField(upload_to='resume/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensure only one profile exists
        if not self.pk and Profile.objects.exists():
            raise Exception('Only one Profile instance allowed.')
        super().save(*args, **kwargs)


class SkillCategory(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, default='⚙️', help_text='Emoji icon')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Skill Categories'
        ordering = ['order']

    def __str__(self):
        return self.name


class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.category.name} — {self.name}'


class Experience(models.Model):
    role = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100, default='Bangalore, India')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text='Leave blank if current job')
    is_current = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-start_date']

    def __str__(self):
        return f'{self.role} @ {self.company}'

    @property
    def period(self):
        start = self.start_date.strftime('%b %Y').upper()
        end = 'PRESENT' if self.is_current else self.end_date.strftime('%b %Y').upper()
        return f'{start} — {end}'


class ExperiencePoint(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='points')
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.experience.role}: {self.text[:50]}'


class Education(models.Model):
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()
    score = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-end_year']

    def __str__(self):
        return f'{self.degree} — {self.institution}'


class Certification(models.Model):
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    title        = models.CharField(max_length=200)
    slug         = models.SlugField(unique=True)
    description  = models.TextField()
    problem      = models.TextField(blank=True, help_text="What problem does it solve?")
    outcome      = models.TextField(blank=True, help_text="Measurable result e.g. 40% faster")
    demo_url     = models.URLField(blank=True)
    github_url   = models.URLField(blank=True)
    cover_image  = models.ImageField(upload_to='projects/', blank=True, null=True)
    tech_stack   = models.JSONField(default=list, help_text='["Django","PostgreSQL","Redis"]')
    github_stars = models.IntegerField(default=0)
    is_featured  = models.BooleanField(default=False)
    order        = models.IntegerField(default=0)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class Scenario(models.Model):
    """A scenario card on the Architecture Decision Lab page.

    `key` must match a scenario key in architecture-lab.js (e.g. 'notification',
    'payments', 'media') so the JS can look up the matching stage/decision data
    for whichever card is opened.
    """
    key               = models.SlugField(unique=True, help_text="Must match a scenario key in architecture-lab.js, e.g. 'notification'")
    number            = models.CharField(max_length=10, help_text="e.g. '01'")
    difficulty        = models.CharField(max_length=100, help_text="e.g. 'SENIOR / SYSTEM DESIGN'")
    title             = models.CharField(max_length=200)
    description       = models.TextField()
    requirement_chips = models.JSONField(default=list, help_text='["10M events/day","Retries + dedupe"]')
    journey_title     = models.CharField(max_length=200, blank=True, help_text="Heading shown once the scenario is opened, e.g. 'Notification delivery, from first principles.'")
    order             = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Stage(models.Model):
    """One step (requirements / initial / bottleneck / evolved) of a scenario's architecture journey."""
    STAGE_CHOICES = [
        ('requirements', 'Requirements'),
        ('initial', 'Start Simple'),
        ('bottleneck', 'Find Limits'),
        ('evolved', 'Evolve'),
    ]
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='stages')
    key      = models.CharField(max_length=20, choices=STAGE_CHOICES)
    mode     = models.CharField(max_length=100, help_text="e.g. 'FOUNDATION'")
    title    = models.CharField(max_length=200, help_text="e.g. '01 — Frame the constraints'")
    text     = models.TextField()
    order    = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ['scenario', 'key']

    def __str__(self):
        return f'{self.scenario.key} / {self.key}'


class StagePoint(models.Model):
    """A bullet point under a stage's explanation."""
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='points')
    text  = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text[:50]


class StageNode(models.Model):
    """One component shown in a stage's architecture diagram, e.g. 'KAFKA'."""
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='nodes')
    name  = models.CharField(max_length=100, help_text="Must match a Component name to power the inspector, e.g. 'KAFKA'")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Component(models.Model):
    """Shared component-inspector info, looked up by name from any stage's diagram nodes."""
    name         = models.CharField(max_length=100, unique=True, help_text="Must match a StageNode name, e.g. 'KAFKA'")
    display_name = models.CharField(max_length=100)
    problem      = models.TextField()
    decision     = models.TextField()
    tradeoff     = models.TextField()
    alternatives = models.TextField()

    class Meta:
        ordering = ['display_name']

    def __str__(self):
        return self.display_name


class Decision(models.Model):
    """A card in the 'Decisions, not dogma' section."""
    title        = models.CharField(max_length=200)
    problem      = models.TextField()
    decision     = models.TextField()
    detail       = models.TextField()
    alternatives = models.TextField()
    order        = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class FailureMode(models.Model):
    """A button/result pair in the 'Break the system' resilience section."""
    name     = models.CharField(max_length=200, help_text="e.g. 'Kafka goes down'")
    impact   = models.CharField(max_length=200)
    response = models.TextField()
    recovery = models.TextField()
    order    = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class ArchitectureDecisionRecord(models.Model):
    """An entry in the ADR log."""
    identifier = models.CharField(max_length=20, help_text="e.g. 'ADR-001'")
    title      = models.CharField(max_length=300)
    detail     = models.TextField()
    order      = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'ADR'
        verbose_name_plural = 'ADRs'

    def __str__(self):
        return f'{self.identifier}: {self.title}'


class TrafficMetric(models.Model):
    """Simulated metrics for one position (0-3) of the traffic slider."""
    level         = models.PositiveIntegerField(unique=True, help_text='0-3, matches the traffic slider position')
    traffic_label = models.CharField(max_length=50, help_text="e.g. '10K events/day'")
    events        = models.CharField(max_length=50, help_text="e.g. '10,000'")
    throughput    = models.CharField(max_length=50)
    latency       = models.CharField(max_length=50)
    error_rate    = models.CharField(max_length=50)
    queue_lag     = models.CharField(max_length=50)
    db_load       = models.CharField(max_length=50)

    class Meta:
        ordering = ['level']

    def __str__(self):
        return self.traffic_label


class SimulatorPlan(models.Model):
    """One recommended architecture tier (0-3) for a scenario's 'what would you change' simulator."""
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='simulator_plans')
    tier     = models.PositiveIntegerField(help_text='0-3, matches the computed pressure tier')
    name     = models.CharField(max_length=200)
    diagram  = models.TextField()

    class Meta:
        ordering = ['tier']
        unique_together = ['scenario', 'tier']

    def __str__(self):
        return f'{self.scenario.key} / tier {self.tier}'


class SimulatorBottleneck(models.Model):
    """Shared bottleneck description per simulator pressure tier (0-3)."""
    tier = models.PositiveIntegerField(unique=True)
    text = models.CharField(max_length=300)

    class Meta:
        ordering = ['tier']

    def __str__(self):
        return f'Tier {self.tier}: {self.text}'


class CurrentlyWorking(models.Model):
    """Singleton — only one active record shown."""
    title       = models.CharField(max_length=200, help_text="What are you building/learning?")
    description = models.TextField(blank=True)
    type        = models.CharField(max_length=50, choices=[
        ('building', 'Building'),
        ('learning', 'Learning'),
        ('contributing', 'Contributing'),
        ('reading', 'Reading'),
    ], default='building')
    tech_tags   = models.JSONField(default=list, help_text='["FastAPI","LangChain"]')
    link        = models.URLField(blank=True)
    progress    = models.IntegerField(default=0, help_text="0-100 percent")
    is_active   = models.BooleanField(default=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Currently Working On"
        verbose_name_plural = "Currently Working On"

    def __str__(self):
        return self.title