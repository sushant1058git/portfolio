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
